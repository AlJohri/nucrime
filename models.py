from pymongo import MongoClient
client = MongoClient()
db = client.nucrime
incidents = db.incidents
tickets = db.tickets