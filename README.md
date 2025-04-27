<h1 align = "center">🎓 University Management System APIs<h1>
<h3>This is a Flask-based REST API project for accessing university departments, students, and courses data from a MySQL database.  
It provides easy-to-use endpoints, Swagger API documentation, and a modern web interface for testing.</h3>

---
##🚀 Features
- RESTful API GET endpoints for:
  - **Departments** with instructor details
  - **Students** with course enrollment details
  - **Courses** with instructor teaching details
- **Swagger API Documentation** (`Flasgger` powered)
- **MySQL database** integration
- **Responsive Web Interface** (HTML/CSS)
- Modular code structure using Flask **Blueprints**
- Pagination support for all APIs

---

## 📦 Prerequisites

- Python 3.x
- MySQL database (with university data loaded)
- `pip` package manager

---

## 🛠 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RadhikaIyengar/University-Information-System.git
   cd <project-directory> 

## How to Run the code?

- Create and activate a virtual environment

- python -m venv venv
- On Windows: venv\Scripts\activate
- Install dependencies:
    - pip install -r requirements.txt
- Configure connection.py file with correct MySQL credentials (host, username, password, database name).


## Project Structure

![Project Structure](assets\Project Structure.png)

## To run the Application

- Start the flask server by typing the following command in the terminal -

- python app.py

- Access the endpoints:

**Web Portal: http://127.0.0.1:5000**

**Swagger API Documentation: http://127.0.0.1:5000/apidocs/**

🔥 Web Interface
The web interface provides quick links to:

- Departments API

- Students API

- Courses API

- Embedded Swagger API documentation

## API Endpoints

All APIs support pagination via:

**page(default = 1)**

**page_size(default = 10)**

**Common JSON response structure**

{
  "code": 1,
  "msg": "Success",
  "data": {
    "records": [],
    "total": 0
  }
}

🧬 Departments
Endpoint: /departments

Returns: List of departments and associated instructors.

🧑‍🏫 Students
Endpoint: /students

Returns: List of students and enrolled courses.

📚 Courses
Endpoint: /courses

Returns: List of courses and teaching instructors.

⚙️ Dependencies
Flask - Web framework
Flasgger - Swagger API Documentation