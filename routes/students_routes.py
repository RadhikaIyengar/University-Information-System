from flask import Blueprint, request,jsonify
from flasgger import swag_from
from models.students import get_students_with_courses
from utils.pagination import paginate
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)


students_bp = Blueprint('students',__name__)


@students_bp.route('/students', methods=['GET'])
@swag_from({
    'tags': ['Students'],
    'description': 'Returns list of students with enrolled courses.',
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'description': 'Page number for pagination',
            'default': 1,
        },
        {
            'name': 'page_size',
            'in': 'query',
            'type': 'integer',
            'description': 'Number of records per page',
            'default': 10,
        }
    ],
    'responses': {
        '200': {
            'description': 'List of students with enrolled courses',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer'},
                    'msg': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'records': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'student_id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'courses': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'course_id': {'type': 'integer'},
                                                    'course_name': {'type': 'string'},
                                                    'instructor': {'type': 'string'}
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            'total': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        '400': {
            'description': "Error: 'page' and 'page_size' must be integers."
        },
        '404': {
            'description': 'Error: No students found.'
        },
        '500': {
            'description': 'Error: Unable to fetch student data from the database.'
        }
    }
})
def students():
    try:
        # Get 'page' and 'page_size' from the request, with defaults
        page = request.args.get('page', 1)
        page_size = request.args.get('page_size', 10)

        # Validate if 'page' and 'page_size' are integers
        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            return jsonify({
                "code": 0,
                "msg": "Error: 'page' and 'page_size' must be integers.",
                "data": {}
            }), 400

        # Check for missing or invalid values in query parameters
        if page < 1 or page_size < 1:
            return jsonify({
                "code": 0,
                "msg": "Error: 'page' and 'page_size' must be positive integers.",
                "data": {}
            }), 400

        # Fetch the data
        try:
            data = get_students_with_courses()
        except Exception as db_error:
            logging.error(f"Database error: {db_error}")
            return jsonify({
                "code": 0,
                "msg": "Error: Unable to fetch student data from the database.",
                "data": {}
            }), 500

        if not data:
            # If no data is returned, return an error response
            return jsonify({
                "code": 0,
                "msg": "Error: No students found.",
                "data": {
                    "records": [],
                    "total": 0
                }
            }), 404

        # Paginate the data
        paginated_data = paginate(data, page, page_size)

        # Check if paginated data has records
        if not paginated_data['data']['records']:
            return jsonify({
                 "code": 0,
                 "msg": "Error: No students found.",
                 "data": {}
            }), 404

        # Return the paginated data as a successful response
        return jsonify({
            "code": paginated_data['code'],
            "msg": paginated_data['msg'],
            "data": paginated_data['data'],
        })

    except Exception as e:
        # If an unexpected error occurs, log the error and return a error message
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({
            "code": 0,
            "msg": "Error: Something went wrong. Please try again later.",
            "data": {}
        }), 500
    
#To check the exception is handled well or not
#def get_students_with_courses():
    #raise Exception("Simulated database error")