from mongo_connection import db
from pymongo.errors import PyMongoError

if db is None:
    print("MongoDB connection is unavailable.")
    exit()

# --- Departments ---
try:
    departments_collection = db["departments"]
    dept_count = departments_collection.count_documents({})
    cs_dept = departments_collection.find_one({"dept_name": "CompSci"})
    num_cs_instructors = len(cs_dept["instructors"]) if cs_dept and "instructors" in cs_dept else 0

    print("\nDepartments:")
    print(f"Total documents: {dept_count}")
    print(f"Instructors in CompSci: {num_cs_instructors}")
except PyMongoError as e:
    print(f"Error accessing departments collection: {e}")

# --- Students ---
try:
    students_collection = db["students"]
    student_count = students_collection.count_documents({})
    peter = students_collection.find_one({"name": "Peter Lynch"})
    fall_2023_courses = 0
    if peter and "courses" in peter:
        for course in peter["courses"]:
            if course.get("semester") == "Fall" and course.get("year") == 2023:
                fall_2023_courses += 1

    print("\nStudents:")
    print(f"Total documents: {student_count}")
    print(f"Peter Lynch's Fall 2023 courses: {fall_2023_courses}")
except PyMongoError as e:
    print(f"Error accessing students collection: {e}")

# --- Courses ---
try:
    courses_collection = db["courses"]
    course_count = courses_collection.count_documents({})
    course_doc = courses_collection.find_one({"title": "Hands-on data science"})

    print("\nCourses:")
    print(f"Total documents: {course_count}")

    if course_doc and "instructors" in course_doc:
        print("Instructor(s) for 'Hands-on data science':")
        for instr in course_doc["instructors"]:
            print(f"- {instr['name']} (Semester: {instr['semester']}, Year: {instr['year']})")
    else:
        print("Course 'Hands-on data science' not found or no instructors listed.")
except PyMongoError as e:
    print(f"Error accessing courses collection: {e}")
