from dataclasses import dataclass
from typing import Optional


@dataclass
class InvestmentRecord:
    """
    Model representing an investment record with all necessary fields
    """
    title: str
    slug: str
    minimum_investment: float
    annual_yield: float
    due_date: str
    extraction_date: str

    def to_dict(self) -> dict:
        """
        Converts the investment record to a dictionary
        """
        return {
            'title': self.title,
            'slug': self.slug,
            'minimum_investment': self.minimum_investment,
            'annual_yield': self.annual_yield,
            'due_date': self.due_date,
            'extraction_date': self.extraction_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'InvestmentRecord':
        """
        Creates an InvestmentRecord instance from a dictionary
        """
        return cls(
            title=data.get('title', ''),
            slug=data.get('slug', ''),
            minimum_investment=data.get('minimum_investment'),
            annual_yield=data.get('annual_yield'),
            due_date=data.get('due_date'),
            extraction_date=data.get('extraction_date', '')
        )

    def validate(self) -> bool:
        """
        Validates if the record has the minimum required fields
        """
        return bool(self.title and self.slug and self.extraction_date)


@dataclass
class Investment:
    """
    Model representing the main investment entity stored in investments_collection
    """
    title: str
    slug: str
    created_at: str
    updated_at: str
    id: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Converts the investment to a dictionary for Firestore storage
        """
        data = {
            'title': self.title,
            'slug': self.slug,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self.id:
            data['id'] = self.id
        return data


@dataclass
class InvestmentDetails:
    """
    Model representing investment details stored in investment_details_collection
    """
    investment_id: str
    minimum_investment: Optional[float]
    annual_yield: Optional[float]
    due_date: Optional[str]
    extraction_date: str
    created_at: str
    id: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Converts the investment details to a dictionary for Firestore storage
        """
        data = {
            'investment_id': self.investment_id,
            'minimum_investment': self.minimum_investment,
            'annual_yield': self.annual_yield,
            'due_date': self.due_date,
            'extraction_date': self.extraction_date,
            'created_at': self.created_at
        }
        if self.id:
            data['id'] = self.id
        return data
