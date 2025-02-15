#!/usr/bin/python3
"""Storage Module"""


import os
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage


"""Storage type based on env VAR"""
if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
