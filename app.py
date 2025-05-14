from flask import Flask, render_template
from flasgger import Swagger
from routes.departments_routes import departments_bp
from routes.students_routes import students_bp
from routes.courses_routes import courses_bp
from storage.redis_connection import r
from redis.exceptions import ConnectionError

# Check Redis connection
try:
    r.ping()
except ConnectionError as e:
    print(f"Redis connection failed: {e}")
    exit("Exiting: Redis is not available.")

app = Flask(__name__)

# Initialize Swagger
swagger = Swagger(app)

# Register your blueprints
app.register_blueprint(departments_bp)
app.register_blueprint(students_bp)
app.register_blueprint(courses_bp)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error occurred."}, 500

if __name__ == '__main__':
    print("Flask app is starting...")
    app.run(debug=True, port=8000)
