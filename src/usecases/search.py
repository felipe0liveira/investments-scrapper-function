import logging

from src.providers.scrapper import Scrapper
from src.providers.storage import Storage


class SearchUseCase:
    def __init__(self, query: str):
        self.query = query
        self.storage = Storage()

    def execute(self):
        logger = logging.getLogger(__name__)
        logger.info("Starting web scraping.")

        scrapper = Scrapper(headless=False)
        investments_list = scrapper.execute()

        if len(investments_list) == 0:
            logger.warning("No records found.")
            return {"message": "scrapped", "records_found": 0}

        logger.info(f"Number of records on website table: {len(investments_list)}")

        db_records = self.storage.analize(investments_list)
        self.storage.execute(db_records)

        logger.info(f"{len(db_records)} records sent to Firestore.")

        return {"message": "scrapped", "records_processed": len(db_records)}
