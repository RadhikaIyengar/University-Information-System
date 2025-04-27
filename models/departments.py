from Database.connection import get_connection

def get_departments_with_instructors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Return results as dictionaries
    query = """
        SELECT d.dept_name, d.building, d.budget, 
               i.id AS instructor_id, i.name AS instructor_name, i.salary AS instructor_salary
        FROM department d
        LEFT JOIN instructor i ON d.dept_name = i.dept_name
        ORDER BY d.dept_name
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    # Group by department
    departments = {}
    for row in data:
        dept_name = row['dept_name']
        if dept_name not in departments:
            departments[dept_name] = {
                "dept_name": dept_name,
                "building": row['building'],
                "budget": row['budget'],
                "instructors": []
            }
        
        if row['instructor_id'] is not None:
            instructor = {
                "id": row['instructor_id'],
                "name": row['instructor_name'],
                "salary": row['instructor_salary']
            }
            departments[dept_name]["instructors"].append(instructor)

    return list(departments.values())
