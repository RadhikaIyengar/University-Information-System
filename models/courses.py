from Database.connection import get_connection

def get_courses_with_instructors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    course_query = """
        SELECT course_id, title, dept_name, credits
        FROM course
    """
    cursor.execute(course_query)
    courses_data = cursor.fetchall()

    courses = {}

    for course in courses_data:
        course_id = course['course_id']

        # Initialize course entry
        courses[course_id] = {
            "course_id": course_id,
            "dept_name": course['dept_name'],
            "title": course['title'],
            "instructors": []
        }

        # Now fetch instructors teaching this course
        instructor_query = """
            SELECT t.ID AS instructor_id, i.name AS instructor_name,
                   t.sec_id AS section, t.semester, t.year
            FROM teaches t
            JOIN instructor i ON t.ID = i.ID
            WHERE t.course_id = %s
        """
        cursor.execute(instructor_query, (course_id,))
        instructors_data = cursor.fetchall()

        for instructor in instructors_data:
            instructor_info = {
                "instructor_id": str(instructor['instructor_id']),
                "name": instructor['instructor_name'],
                "section": instructor['section'],
                "semester": instructor['semester'],
                "year": instructor['year']
            }
            courses[course_id]['instructors'].append(instructor_info)

    conn.close()

    return {
        "code": 1,
        "data": {
            "records": list(courses.values()),
            "total": len(courses)
        },
        "msg": "Success"
    }
