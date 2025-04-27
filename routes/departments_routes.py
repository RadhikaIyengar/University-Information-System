from flask import Blueprint, request,jsonify
from flasgger import swag_from
from models.departments import get_departments_with_instructors
from utils.pagination import paginate
import logging

logging.basicConfig(level=logging.ERROR)


departments_bp = Blueprint('departments',__name__)

@departments_bp.route('/departments', methods=['GET'])
@swag_from({
    'tags': ['Departments'],
    'description': 'Returns list of departments with associated instructors.',
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
            'description': 'List of departments with associated instructors',
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
                                        'department_id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'instructors': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'instructor_id': {'type': 'integer'},
                                                    'name': {'type': 'string'}
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
            'description': 'Error: No departments found.'
        },
        '500': {
            'description': 'Error: Unable to fetch department data from the database.'
        }
    }
})
def departments():
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
            data = get_departments_with_instructors()
        except Exception as db_error:
            logging.error(f"Database error: {db_error}")
            return jsonify({
                "code": 0,
                "msg": "Error: Unable to fetch department data from the database.",
                "data": {}
            }), 500

        if not data:
            # If no data is returned, return an error response
            return jsonify({
                "code": 0,
                "msg": "Error: No departments found.",
                "data": {
                    "records": [],
                    "total": 0
                }
            }), 404

        # Paginate the data
        paginated_data = paginate(data, page, page_size)

        if not paginated_data['data']['records']:
            return jsonify({
                 "code": 0,
                 "msg": "Error: No departments found.",
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
#def get_departments_with_instructors():
    #raise Exception("Simulated database error")