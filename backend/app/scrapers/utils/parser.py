import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def soup_text(html: str) -> str:
    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)


def first_match(pattern: str, text: str, default=None):
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return default
    return match.group(1)


def first_int(pattern: str, text: str, default=None):
    value = first_match(pattern, text, default=None)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def first_float(pattern: str, text: str, default=None):
    value = first_match(pattern, text, default=None)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def page_title(html: str, default: str | None = None) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    heading = soup.find(["h1", "h2"])
    if heading:
        return heading.get_text(" ", strip=True)
    return default


def internal_links_by_keywords(html: str, base_url: str, keywords: list[str], limit: int = 8) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    matches: list[dict] = []
    seen: set[str] = set()
    lowered = [keyword.lower() for keyword in keywords]

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        text = anchor.get_text(" ", strip=True)
        haystack = f"{text} {href}".lower()
        if not any(keyword in haystack for keyword in lowered):
            continue
        absolute_url = urljoin(base_url, href)
        if absolute_url in seen:
            continue
        seen.add(absolute_url)
        matches.append({"text": text or absolute_url, "url": absolute_url})
        if len(matches) >= limit:
            break
    return matches
