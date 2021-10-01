import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb://library:pencil1234@44.199.16.91:29017/?authSource=admin")
db = cluster["lapiz"]
#collection = db["person"]
collection = db["student"]

results = collection.find()

for r in results:
    print(r)
