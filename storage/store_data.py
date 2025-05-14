import sys, os
import requests
import json
from pymongo.errors import PyMongoError
import redis

# Setup paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.redis_connection import r
from mongo_connection import db

# Fetch all paginated data from API
def fetch_all_data(api_url):
    all_data = []
    page = 1
    while True:
        try:
            response = requests.get(f"{api_url}?page={page}", timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {api_url}?page={page}: {e}")
            break

        try:
            response_json = response.json()
        except json.JSONDecodeError:
            print(f"Invalid JSON response from {api_url}?page={page}")
            break

        print(f"\nFull JSON Response from {api_url}?page={page}")
        print(json.dumps(response_json, indent=2))

        data = response_json.get("data", {})
        page_data = data.get("records", [])
        if not page_data:
            break
        all_data.extend(page_data)
        page += 1
    return all_data

# Base API URL
BASE_URL = "http://127.0.0.1:8000"

# Fetch data
departments_data = fetch_all_data(f"{BASE_URL}/departments")
students_data = fetch_all_data(f"{BASE_URL}/students")
courses_data = fetch_all_data(f"{BASE_URL}/courses")

print("Retrieved Data:")
print(f"Departments: {len(departments_data)}")
print(f"Students: {len(students_data)}")
print(f"Courses: {len(courses_data)}")

# Redis Insertion with Error Handling
def safe_redis_set(key, value):
    try:
        if not r.exists(key):
            r.set(key, json.dumps(value))
    except redis.exceptions.RedisError as e:
        print(f"Redis error for key '{key}': {e}")

for dept in departments_data:
    key = f"departments:{dept['dept_name']}"
    safe_redis_set(key, dept)

for student in students_data:
    key = f"students:{student['name']}"
    safe_redis_set(key, student)

for course in courses_data:
    key = f"courses:{course['title']}"
    safe_redis_set(key, course)

# MongoDB Insertion with Error Handling
def safe_mongo_insert(collection, query_filter, document):
    try:
        if not db[collection].find_one(query_filter):
            db[collection].insert_one(document)
    except PyMongoError as e:
        print(f"MongoDB error in collection '{collection}': {e}")

for dept in departments_data:
    safe_mongo_insert("departments", {"dept_name": dept["dept_name"]}, dept)

for student in students_data:
    safe_mongo_insert("students", {"id": student["id"]}, student)

for course in courses_data:
    safe_mongo_insert("courses", {"course_id": course["course_id"]}, course)

print("Data inserted without duplicates into Redis and MongoDB.")
