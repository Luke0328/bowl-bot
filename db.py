import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
DB_PWD = os.getenv('DB_PWD')
URI = 'mongodb+srv://luke0328:{0}@cluster0.45uf3t7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'.format(DB_PWD)

class Database:
    """class to interact with the database"""
    def __init__(self):
        self.client = pymongo.MongoClient(URI)
        self.db = self.client.bowl_bot_db
        self.players = self.db.players
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def add_score(self, score):
        test = {
            'name': 'Luke',
            'scores': []
        }
        res = self.players.insert_one(test)

db = Database()
db.add_score(1)