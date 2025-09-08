import logging
from src.core.settings import Settings
from src.scrapper import Scrapper
from src.analizer import analize
from src.storage import Storage


def main():
    Settings()

    logger = logging.getLogger(__name__)
    logger.info("Starting web scraping.")
    scrapper = Scrapper(headless=False)
    filename, length = scrapper.execute()

    if length == 0:
        logger.warning("No records found.")
        return

    logger.info(f"File saved: {filename}")
    logger.info(f"Number of records: {length}")

    db_records = analize(filename)
    storage = Storage()
    storage.execute(db_records)

    logger.info(f"{len(db_records)} records sent to Firestore.")


if __name__ == "__main__":
    main()
