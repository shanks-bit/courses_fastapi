from fastapi.testclient import TestClient
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from bson import ObjectId
import pytest
from main import app

client = TestClient(app)
uri = "mongodb+srv://shashankdhanai83:Shanks123@shashank83.z6mdljc.mongodb.net/?retryWrites=true&w=majority&appName=Shashank83"

# Create a new client and connect to the server
client1 = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the 'Discuss' database
db = client1.KIBO

# Access the 'kibo_collection' collection within the 'Discuss' database
collection = db['kibo_collection']




def test_get_courses():
    response = client.get("/courses")
    assert response.status_code == 200

def test_get_courses_alphabetical():
    response = client.get("/courses?sort_by=alphabetical")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0
    assert sorted(courses, key=lambda a: a['name']) == courses


def test_get_courses_date():
    response = client.get("/courses?sort_by=date")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0
    assert sorted(courses, key=lambda a: a['date'], reverse=True) == courses

def test_get_courses_rating():
    response = client.get("/courses?sort_by=rating")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0
    assert sorted(courses, key=lambda a: a['rating']['total'], reverse=True) == courses

def test_get_course_by_id_exists():
    response = client.get("/courses/66b42dbc27c968ebf2ceabca")
    assert response.status_code == 200
    course = response.json()
    # get the course from database
    courseDb = collection.find_one({'_id': ObjectId('66b42dbc27c968ebf2ceabca')})
    # get the name of the course from database
    nameDb = courseDb['name']
    # get the name of the course from response
    nameResp = course['name']
    # compare them
    assert nameDb == nameResp
     
     
def test_get_course_by_id_not_exists():
    response = client.get("/courses/67b42dbc27c968ebf2ceabca")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Course unavilable'}

def test_get_chapter():
    response = client.get("/courses/66b42dbc27c968ebf2ceabca/4")
    assert response.status_code == 200
    chapter = response.json()
    assert chapter['name'] == 'The Exponential Function'
    assert chapter['text'] == 'Highlights of Calculus'
    
    
def test_get_chapter_not_exists():
    response = client.get("/courses/66b42dbc27c968ebf2ceabca/578")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Chapter unavilable'}
    
    
def test_rate_chapter():
    course_id = "66b42dbc27c968ebf2ceabca"
    chapter_id = "1"
    rating = 1

    response = client.post(f"/courses/{course_id}/{chapter_id}?rating={rating}")

    assert response.status_code == 200

    # Check if the response body has the expected structure
    assert "name" in response.json()
    assert "rating" in response.json()
    assert "total" in response.json()["rating"]
    assert "count" in response.json()["rating"]

    assert response.json()["rating"]["total"] > 0
    assert response.json()["rating"]["count"] > 0
     
def test_rate_chapter_not_exists():
    response = client.post("/courses/66b42dbc27c968ebf2ceabca/578/rate", json={"rating": 1})
    assert response.status_code == 404
    assert response.json() == {'detail': 'unavilable'}