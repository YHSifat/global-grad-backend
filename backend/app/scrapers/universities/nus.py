from app.scrapers.base import UniversityScraper, ScrapedUniversity
from app.scrapers.utils.fetcher import fetch_html
from app.scrapers.utils.parser import soup_text, first_int


class NusScraper(UniversityScraper):
    source_key = "nus"
    source_url = "https://www.nus.edu.sg/"

    def scrape(self) -> ScrapedUniversity:
        html = fetch_html(self.source_url)
        text = soup_text(html)
        return ScrapedUniversity(
            name="National University of Singapore",
            ranking=first_int(r"ranking\D+(\d+)", text),
            location="Singapore",
            website=self.source_url,
            country="Singapore",
            city="Singapore",
            programs=[],
            professors=[],
            scholarships=[],
        )
