""" if file storage or db storage"""
from os import getenv


# retrieve env for db storage
if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
# retrieve env for file storage
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# reload to make sure its up to date, like refreshing
storage.reload()
