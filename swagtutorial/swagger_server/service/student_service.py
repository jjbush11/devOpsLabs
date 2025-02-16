import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB using an environment variable or default to localhost.
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
# Create a database
db = client["student_db"]
# Creates a collection, which is like a table
students_collection = db["students"]


def add(student=None):
    # Creates a query to check if student already exists
    query = {"first_name": student.first_name, "last_name": student.last_name}
    existing = students_collection.find_one(query)
    if existing:
        return 'already exists', 409

    # Insert the new student and convert the inserted_id to a string.
    result = students_collection.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)
    print("Student Added!")
    return student.student_id


def get_by_id(student_id=None, subject=None):
    try:
        # Convert the student_id from string to ObjectId for querying.
        student = students_collection.find_one({"_id": ObjectId(student_id)})
    except Exception:
        return 'not found', 404

    if not student:
        return 'not found', 404

        # Convert the ObjectId to string so it can be returned in JSON.
    student['student_id'] = str(student['_id'])
    return student


def delete(student_id=None):
    try:
        result = students_collection.delete_one({"_id": ObjectId(student_id)})
    except Exception:
        return 'not found', 404

    if result.deleted_count == 0:
        return 'not found', 404
    return student_id
