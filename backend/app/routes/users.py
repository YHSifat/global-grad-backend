from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User, Role
from app.schemas.user import UserCreate, UserRead, UserUpdate, Role as RoleSchema, TokenData
from app.core import security

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    role_value = user.role.value if hasattr(user.role, "value") else user.role
    hashed = security.get_password_hash(user.password) if user.password else None
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed,
        role=Role(role_value),
        gpa=user.gpa,
        ielts=user.ielts,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/students", response_model=UserRead)
def create_student(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = security.get_password_hash(user.password) if user.password else None
    # Force role to student (regular user)
    try:
        student_role = Role.STUDENT
    except AttributeError:
        student_role = Role("student")
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed,
        role=student_role,
        gpa=user.gpa,
        ielts=user.ielts,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserRead])
def list_users(role: Optional[RoleSchema] = None, db: Session = Depends(get_db), _: TokenData = Depends(security.get_current_active_admin)):
    q = db.query(User)
    if role:
        role_value = role.value if hasattr(role, "value") else role
        q = q.filter(User.role == Role(role_value))
    return q.all()

@router.get("/me", response_model=UserRead)
def read_current_user(current_user = Depends(security.get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(security.oauth2_scheme)):
    payload = security.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    role = payload.get("role")
    if role != Role.ADMIN.value:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "deleted"}
