#!/usr/bin/python3
"""WSGI entry point for Gunicorn"""

from 0-hello_route import app

if __name__ == "__main__":
    app.run()

