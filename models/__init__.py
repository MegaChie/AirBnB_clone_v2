#!/usr/bin/python3
"""This module initializes the package and instantiates
the FileStorage and DBStorage objects."""
from models.engine import storage_type
# from models.base_model import BaseModel, Base
# from models.user import User
# from models.place import Place
# from models.city import City  # Import the City class


if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    # Instantiate the FileStorage object
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()

# Optionally, expose models for easy access
__all__ = ['BaseModel', 'User', 'Place', 'City', 'storage']
