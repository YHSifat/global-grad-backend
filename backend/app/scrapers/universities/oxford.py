from app.scrapers.base import UniversityScraper, ScrapedUniversity
from app.scrapers.utils.fetcher import fetch_html
from app.scrapers.utils.parser import soup_text, first_int


class OxfordScraper(UniversityScraper):
    source_key = "oxford"
    source_url = "https://www.ox.ac.uk/"

    def scrape(self) -> ScrapedUniversity:
        html = fetch_html(self.source_url)
        text = soup_text(html)
        return ScrapedUniversity(
            name="University of Oxford",
            ranking=first_int(r"ranking\D+(\d+)", text),
            location="Oxford, United Kingdom",
            website=self.source_url,
            country="United Kingdom",
            city="Oxford",
            programs=[],
            professors=[],
            scholarships=[],
        )
