from flask import Flask, render_template
from flasgger import Swagger
from routes.departments_routes import departments_bp
from routes.students_routes import students_bp
from routes.courses_routes import courses_bp

app = Flask(__name__)

# Initialize Swagger
swagger = Swagger(app)


# Register your blueprints
app.register_blueprint(departments_bp)
app.register_blueprint(students_bp)
app.register_blueprint(courses_bp)

# Add your homepage route
@app.route('/')
def homepage():
    return render_template('home.html') 

if __name__ == '__main__':
    print("Flask app is starting...")
    app.run(debug=True)
