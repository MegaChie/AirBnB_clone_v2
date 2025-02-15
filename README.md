# ![logo](https://user-images.githubusercontent.com/108279441/220420558-12b71945-3e02-4adf-b989-5f8fa1b4c683.png)

# AirBnB Clone V2 - The Holberton B&B

## Overview

Welcome to version 2 of the Holberton School AirBnB clone project. This repository extends the initial console-based management system to include data persistence via a SQL database, a web flask framework for rendering the frontend, and an API for interaction between the frontend and backend. This second version aims to integrate more complex functionalities and a more robust backend architecture suitable for real-world applications.

## Technical Stack

- **Backend Programming**: Python 3, Flask
- **Data Storage**: MySQL (Development), File Storage (JSON files)
- **API**: Flask RESTful
- **Testing**: Python unittest for backend testing
- **Frontend**: HTML, CSS, JavaScript (Bootstrap for styling)
- **Version Control**: Git, GitHub

## Repository Contents by Project Task

| Task Number | Feature              | File(s)                                   | Description                                                  |
|-------------|----------------------|-------------------------------------------|--------------------------------------------------------------|
| 0           | Authors/README File  | `AUTHORS`, `README.md`                    | Project authors and markdown README.                         |
| 1           | Pep8                 | N/A                                       | Ensures all code is compliant with PEP8 standards.           |
| 2           | Unit Testing         | `/tests`                                  | All backend code is accompanied by unittests.                |
| 3           | BaseModel            | `/models/base_model.py`                   | Defines a parent class for future class inheritance.         |
| 4           | File Storage         | `/models/engine/file_storage.py`          | Manages JSON serialization and deserialization of objects.   |
| 5           | Console              | `console.py`                              | Updated console for object management via commands.          |
| 6           | Web Flask            | `/web_flask`                              | Introduces Flask application setups for the web framework.   |
| 7           | Database Storage     | `setup_mysql_dev.sql`                     | Scripts for setting up MySQL database for development.       |
| 8           | Flask API            | `/api/`                                   | Flask application to create an API for object manipulation.  |
| 9           | Frontend Integration | `/web_static`                             | Contains static HTML and CSS files for the website frontend. |

## General Usage

### Starting the Console

#```bash
/AirBnB_clone_v2$ ./console.py
(hbnb) help

Commands Overview
create: Creates a new instance.
show: Displays an instance based on UUID.
destroy: Deletes an instance based on UUID.
all: Shows all instances stored.
update: Updates an instance based on the class name and UUID.
quit: Exits the console.
EOF: Also exits the console.
Running Web Flask
Navigate to the web_flask directory and run the Flask application.

$ FLASK_APP=my_application.py FLASK_ENV=development flask run

This command starts the Flask web server in development mode.


### Part 3: Installation Instructions
#```markdown
## Installation

Clone the repository to your local machine:

#```bash
$ git clone https://github.com/MicoBledsoe/holbertonschool-AirBnB_clone_v2.git
$ cd holbertonschool-AirBnB_clone_v2

Set up the database:
$ mysql -u root -p < setup_mysql_dev.sql

Environment Variables
Set the following environment variables in your .env file:
FLASK_APP=run.py
FLASK_ENV=development
DB_USERNAME=test_user
DB_PASSWORD=test_password
DB_HOST=localhost


### Part 4: Additional Information
#```markdown
## Contributors and Acknowledgment

- Original Authors: [Justin Majetich](https://github.com/justinmajetich), [Enrique Nobrega](https://github.com/eNobreg)
- Current Collaborators: [Mico Bledsoe](https://github.com/MicoBledsoe), [Jobaby](https://github.com/jobabyyy)

This project is part of the Holberton School curriculum aimed at introducing students to fundamental software engineering principles including data handling, APIs, front-end development, and system management.

## Initial Authors:
(https://github.com/justinmajetich)

(https://github.com/eNobreg)

## Collaborators:
(https://github.com/MicoBledsoe)

(https://github.com/jobabyyy)
