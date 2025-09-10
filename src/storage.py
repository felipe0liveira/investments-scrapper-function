from datetime import datetime
import logging
from zoneinfo import ZoneInfo
from src.core.database import Database
from src.models import Investment, InvestmentDetails, InvestmentRecord


class Storage:
    def __init__(self):
        self.database = Database()
        self.collection = self.database.investments_collection
        self.details_collection = self.database.investment_details_collection
        self.logger = logging.getLogger(__name__)

    def execute(self, records: list[InvestmentRecord]):
        """
        Processes investment records:
        1. Checks if the slug already exists in investments_collection
        2. If it doesn't exist, creates a new document with title, slug, created_at
        3. Adds details to investment_details_collection
        """
        batch = self.database.db.batch()
        current_time = datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat()
        
        for record in records:
            slug = record.slug
            if not slug:
                self.logger.warning(f"Record missing slug: {record}")
                continue
            
            # Checks if the investment already exists by slug
            investment_doc = self._get_investment_by_slug(slug)
            
            if not investment_doc:
                # Creates new document in investments_collection
                investment_ref = self.collection.document()
                investment_data = Investment(
                    title=record.title,
                    slug=record.slug,
                    created_at=current_time,
                    updated_at=current_time
                )

                batch.set(investment_ref, investment_data.to_dict())
                investment_id = investment_ref.id
                self.logger.info(f"Created new investment: {slug}")
            else:
                # Updates the updated_at field of existing investment
                investment_id = investment_doc.id
                investment_ref = self.collection.document(investment_id)
                batch.update(investment_ref, {'updated_at': current_time})
                self.logger.info(f"Updated investment: {slug}")
            
            # Adds details to investment_details_collection
            details_ref = self.details_collection.document()
            details_data = InvestmentDetails(
                investment_id=investment_id,
                minimum_investment=record.minimum_investment,
                annual_yield=record.annual_yield,
                due_date=record.due_date,
                extraction_date=record.extraction_date,
                created_at=current_time
            )
            batch.set(details_ref, details_data.to_dict())

        # Executes all operations in batch
        batch.commit()
        
        self.logger.info(
            f"Processed {len(records)} records. "
            f"Investments collection now has {self.collection.count().get()[0][0].value} documents."
        )

    def _get_investment_by_slug(self, slug: str):
        """
        Searches for an investment by slug in investments_collection
        """
        try:
            query = self.collection.where('slug', '==', slug).limit(1)
            docs = query.get()
            return docs[0] if docs else None
        except Exception as e:
            self.logger.error(f"Error querying investment by slug {slug}: {e}")
            return None
