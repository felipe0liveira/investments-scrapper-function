from datetime import datetime
import logging
from zoneinfo import ZoneInfo
from src.core.database import Database


class Storage:
    def __init__(self):
        self.database = Database()
        self.collection = self.database.investments_collection
        self.logger = logging.getLogger(__name__)

    def execute(self, records: list[dict]):
        batch = self.database.db.batch()
        for record in records:
            doc_ref = self.collection.document()
            record["created_at"] = datetime.now(
                ZoneInfo("America/Sao_Paulo")
            ).isoformat()
            batch.set(doc_ref, record)
        batch.commit()

        self.logger.info(
            f"Firestore investments_collection now has {self.collection.count().get()[0][0].value} documents."
        )
