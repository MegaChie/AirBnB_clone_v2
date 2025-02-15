mework Guide

## Table of Contents
1. [What is a Web Framework?](#what-is-a-web-framework)
2. [How to Build a Web Framework with Flask](#how-to-build-a-web-framework-with-flask)
3. [How to Define Routes in Flask](#how-to-define-routes-in-flask)
4. [What is a Route?](#what-is-a-route)
5. [How to Handle Variables in a Route](#how-to-handle-variables-in-a-route)
6. [What is a Template?](#what-is-a-template)
7. [How to Create an HTML Response in Flask Using a Template](#how-to-create-an-html-response-in-flask-using-a-template)
8. [How to Create a Dynamic Template (Loops, Conditions)](#how-to-create-a-dynamic-template-loops-conditions)
9. [How to Display Data in HTML from a MySQL Database](#how-to-display-data-in-html-from-a-mysql-database)

## What is a Web Framework?
A web framework is a software framework designed to support the development of web applications including web services, web resources, and web APIs. Frameworks provide a standard way to build and deploy web applications on the World Wide Web.

## How to Build a Web Framework with Flask
Flask is a micro web framework written in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. Flask provides tools, libraries, and technologies that allow you to build a web application.

### Installation
To get started with Flask, first install it using pip:

```sh
pip install Flask
```

# How to Define Routes in Flask

In Flask, routes are defined using the @app.route decorator. This decorator binds a URL to a function which is called whenever the URL is accessed.

```python

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```
# What is a Route?

A route in Flask is a URL pattern that is associated with a specific function. When the URL is accessed, Flask calls the function and returns its response to the client.
How to Handle Variables in a Route

You can handle variables in routes by specifying them in the URL pattern. These variables are then passed to the view function as keyword arguments.

```python

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'
```
# What is a Template?

A template in Flask is a file that contains static data as well as placeholders for dynamic data. Flask uses the Jinja2 templating engine to render templates.
How to Create an HTML Response in Flask Using a Template

To create an HTML response using a template, you use the render_template function provided by Flask.

```python

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
```
### Template (templates/hello.html):

```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
```
# How to Create a Dynamic Template (Loops, Conditions)

Jinja2 templates allow you to use loops and conditions to create dynamic content.

## Example of a loop:

```html

<ul>
  {% for user in users %}
    <li>{{ user.username }}</li>
  {% endfor %}
</ul>
```
### Example of a condition:

```html

{% if user.is_authenticated %}
  <p>Welcome, {{ user.username }}!</p>
{% else %}
  <p>Please log in.</p>
{% endif %}
```
## How to Display Data in HTML from a MySQL Database

To display data from a MySQL database, you first need to query the database and pass the results to a template.
Requirements

### You need the mysqlclient library. Install it using pip:

```sh

pip install mysqlclient
```
**Example:**

```python

import MySQLdb
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    return MySQLdb.connect(user='username', passwd='password', db='database', host='localhost')

@app.route('/users')
def show_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
```
#### Template (templates/users.html):

```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Users</title>
</head>
<body>
    <ul>
      {% for user in users %}
        <li>{{ user[0] }}</li>
      {% endfor %}
    </ul>
</body>
</html>
```
By following this guide, you will have a solid understanding of how to build a basic web application using Flask, how to define routes, handle variables in routes, use templates to create dynamic HTML responses, and display data from a MySQL database.

