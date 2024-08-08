import contextlib
from fastapi import APIRouter, HTTPException, Query
from config.database import collection
import datetime
from bson import ObjectId

courses_root = APIRouter()

#get all courses
@courses_root.get('/courses')
def get_courses(sort_by: str = 'date', domain: str = None):
    # set the rating.total and rating.count to all the courses based on the sum of the chapters rating
    for course in collection.find():
        total = 0
        count = 0
        for chapter in course['chapters']:
            with contextlib.suppress(KeyError):
                total += chapter['rating']['total']
                count += chapter['rating']['count']
        collection.update_one({'_id': course['_id']}, {'$set': {'rating': {'total': total, 'count': count}}})



    # sort by date in descending
    if sort_by == 'date':
        sort_field = 'date'
        sort_order = -1

    # sort by rating in descending
    elif sort_by == 'rating':
        sort_field = 'rating.total'
        sort_order = -1

    # sort by alphabetical in ascending
    else:  
        sort_field = 'name'
        sort_order = 1

    query = {}
    if domain:
        query['domain'] = domain


    courses = collection.find(query, {'name': 1, 'date': 1, 'description': 1, 'domain':1,'rating':1,'_id': 0}).sort(sort_field, sort_order)
    return list(courses)
 

# get course overview
@courses_root.get('/courses/{course_id}')
def get_course(course_id: str):
    course = collection.find_one({'_id': ObjectId(course_id)}, {'_id': 0, 'chapters': 0})
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    try:
        course['rating'] = course['rating']['total']
    except KeyError:
        course['rating'] = 'Not rated' 
    
    return course

# get chapter information
@courses_root.get('/courses/{course_id}/{chapter_id}')
def get_chapter(course_id: str, chapter_id: str):    
    course = collection.find_one({'_id': ObjectId(course_id)}, {'_id': 0})
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[int(chapter_id)]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail='Chapter not found') from e
    return chapter

# rating every chapter by 1 for Positive, -1 For Negative
@courses_root.post('/courses/{course_id}/{chapter_id}')
def rate_chapter(course_id: str, chapter_id: str, rating: int = Query(..., gt=-2, lt=2)):
    course = collection.find_one({'_id': ObjectId(course_id)}, {'_id': 0, })
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[int(chapter_id)]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail='Chapter not found') from e
    try:
        chapter['rating']['total'] += rating
        chapter['rating']['count'] += 1
    except KeyError:
        chapter['rating'] = {'total': rating, 'count': 1}
    collection.update_one({'_id': ObjectId(course_id)}, {'$set': {'chapters': chapters}})
    return chapter 