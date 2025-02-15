#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module instantiates an object of class FileStorage or DBStorage
based on the value of the evironment variable "HBNB_TYPE_STORAGE."
"""
import os

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()

else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
