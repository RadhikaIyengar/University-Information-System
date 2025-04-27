from Database.connection import get_connection

def get_students_with_courses():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
    s.ID, 
    s.name, 
    s.dept_name, 
    s.tot_cred,
    c.course_id, 
    c.title, 
    c.credits,
    sec.sec_id AS section_id, 
    sec.semester, 
    sec.year
FROM 
    student s
LEFT JOIN 
    course c ON s.dept_name = c.dept_name  -- Join student table with course table based on dept_name
LEFT JOIN 
    section sec ON c.course_id = sec.course_id
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    # Group the data by department and student
    students_data = {}

    for row in data:
        dept_name = row['dept_name']
        student_id = row['ID']

        # Ensure department exists in the dictionary
        if dept_name not in students_data:
            students_data[dept_name] = {
                "dept_name": dept_name,
                "students": []
            }

        # Check if student already exists in the department
        student = next((s for s in students_data[dept_name]['students'] if s['id'] == student_id), None)

        if not student:
            student = {
                "id": student_id,
                "name": row['name'],
                "courses": []  # Removed tot_cred as it's not in the final structure
            }
            students_data[dept_name]["students"].append(student)

        # Add course data
        if row['course_id'] is not None:
            course = {
                "course_id": row['course_id'],
                "section_id": row.get('section_id', None),  # Optional: Add section_id if necessary
                "semester": row.get('semester', None),      # Optional: Add semester if necessary
                "year": row.get('year', None)               # Optional: Add year if necessary
            }
            student["courses"].append(course)

    # Convert to the final desired structure
    response_data = {
        "code": 1,
        "data": {
            "records": []
        },
        "msg": "Success"
    }

    # Prepare the records for the response
    for dept_name, dept_data in students_data.items():
        for student in dept_data['students']:
            response_data['data']['records'].append({
                "courses": student['courses'],  # Include only student courses
                "dept_name": dept_name,
                "id": student['id'],
                "name": student['name']
            })

    return response_data
