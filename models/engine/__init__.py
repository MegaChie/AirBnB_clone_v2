#!/usr/bin/python3
""" initialize storage engine """
from os import getenv


# retrieve the env for storage
storage_t = getenv('HBNB_TYPE_STORAGE')

# if it should be stored in db or filestorage
if storage_t == 'db':
	from models.engine.db_storage import DBStorage
	storage = DBStorage()
else:
	from models.engine.file_storage import FileStorage
	storage = FileStorage()

# reload to make sure its up to date, like refreshing
storage.reload()
