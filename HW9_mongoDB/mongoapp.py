import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://Mykola:1111@cluster0.zkdur.mongodb.net/projects_db?retryWrites=true&w=majority"
)
db = cluster["projects_db"]
collection = db["projects"]

# post = {"_id": 0, "content": None, "data": "test_data"}
# collection.insert_one(post)

# post_wo_custom_id = {"content": "something", "data": "some_data"}
# collection.insert_one(post_wo_custom_id)

cur = collection.delete_many(
    {'content': 'modified'}
)

post_count = collection.count_documents({'content': 'modified'})
print(post_count)

results = collection.find({})
print(*results, sep="\n")
