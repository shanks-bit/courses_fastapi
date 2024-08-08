from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

uri = "mongodb+srv://shashankdhanai83:Shanks123@shashank83.z6mdljc.mongodb.net/?retryWrites=true&w=majority&appName=Shashank83"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the 'Discuss' database
db = client.KIBO

# Access the 'kibo_collection' collection within the 'Discuss' database
collection = db['kibo_collection']

# Doing it only one time to import data from courses.json

"""with open('courses.json') as file:
    file_data = json.load(file)


# add rating field to each course
for course in file_data:
    course['rating'] = {'total': 0, 'count': 0}
    
# add rating field to each chapter
for course in file_data:
    for chapter in course['chapters']:
        chapter['rating'] = {'total': 0, 'count': 0}


#inserting all json data into kibo_collection
collection.insert_many(file_data)
print(" json file are imported ")"""

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)




