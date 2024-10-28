#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage

# where to store data
storage = FileStorage()
# save changes, or refresh
storage.reload()
