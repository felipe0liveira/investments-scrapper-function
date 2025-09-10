from google.cloud import firestore


class Database:
    def __init__(self):
        self.db = firestore.Client()
        self.investments_collection = self.db.collection('investments')
        self.investment_details_collection = self.db.collection('investment_details')

