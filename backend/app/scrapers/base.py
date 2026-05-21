from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ScrapedUniversity:
    name: str
    ranking: int | None = None
    location: str | None = None
    website: str | None = None
    country: str | None = None
    city: str | None = None
    programs: List[Dict[str, Any]] = field(default_factory=list)
    professors: List[Dict[str, Any]] = field(default_factory=list)
    scholarships: List[Dict[str, Any]] = field(default_factory=list)


class UniversityScraper(ABC):
    source_key: str = "base"
    source_url: str = ""

    @abstractmethod
    def scrape(self) -> ScrapedUniversity:
        raise NotImplementedError
