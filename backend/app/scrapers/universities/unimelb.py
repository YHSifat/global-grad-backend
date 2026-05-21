from app.scrapers.base import UniversityScraper, ScrapedUniversity
from app.scrapers.utils.fetcher import fetch_html
from app.scrapers.utils.parser import soup_text, first_int, page_title, internal_links_by_keywords


PROGRAM_KEYWORDS = ["program", "course", "study", "degree", "master", "bachelor"]
PROFESSOR_KEYWORDS = ["staff", "people", "academics", "research", "faculty"]
SCHOLARSHIP_KEYWORDS = ["scholarship", "grant", "award", "funding", "bursary"]


class UniMelbScraper(UniversityScraper):
    source_key = "unimelb"
    source_url = "https://www.unimelb.edu.au/"

    def scrape(self) -> ScrapedUniversity:
        html = fetch_html(self.source_url)
        text = soup_text(html)
        title = page_title(html, default="University of Melbourne") or "University of Melbourne"

        program_links = internal_links_by_keywords(html, self.source_url, PROGRAM_KEYWORDS, limit=5)
        professor_links = internal_links_by_keywords(html, self.source_url, PROFESSOR_KEYWORDS, limit=5)
        scholarship_links = internal_links_by_keywords(html, self.source_url, SCHOLARSHIP_KEYWORDS, limit=5)

        programs = [
            {
                "name": item["text"],
                "requirements": "See linked page for details",
                "source": item["url"],
            }
            for item in program_links
        ]
        professors = [
            {
                "name": item["text"],
                "website": item["url"],
                "source": item["url"],
            }
            for item in professor_links
        ]
        scholarships = [
            {
                "name": item["text"],
                "link": item["url"],
                "source": item["url"],
            }
            for item in scholarship_links
        ]

        return ScrapedUniversity(
            name=title,
            ranking=first_int(r"ranking\D+(\d+)", text),
            location="Melbourne, Australia",
            website=self.source_url,
            country="Australia",
            city="Melbourne",
            programs=programs,
            professors=professors,
            scholarships=scholarships,
        )
