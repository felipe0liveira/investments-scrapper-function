from google.cloud import firestore


class Database:
    def __init__(self):
        self.db = firestore.Client()
        self.investments_collection = self.db.collection('investments')

