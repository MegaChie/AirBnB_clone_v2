#!/usr/bin/python3
"""This module defines a class to manage file storage for the HBNB clone."""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of HBNB models in JSON format."""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models (of a class) currently in storage."""
        if cls is not None and not issubclass(cls, (BaseModel, User, Place,
                                                    State, City, Amenity,
                                                    Review)):
            raise TypeError("cls must be a class type")

        if cls:
            return {key: value for key, value in self.__objects.items()
                    if isinstance(value, cls)}
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary."""
        if obj is None:
            raise ValueError("Cannot add NoneType object")
        key = f"{type(obj).__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Saves the storage dictionary to a file."""
        with open(self.__file_path, 'w') as f:
            temp = {key: val.to_dict() for key, val in self.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Loads the storage dictionary from a file."""
        if not os.path.exists(self.__file_path):
            return

        with open(self.__file_path, 'r') as f:
            data = f.read()
            if not data:
                raise ValueError("File is empty")  # Raise ValueError if empty

            temp = json.loads(data)
            classes = {
                'BaseModel': BaseModel,
                'User': User,
                'Place': Place,
                'State': State,
                'City': City,
                'Amenity': Amenity,
                'Review': Review
            }

            for key, val in temp.items():
                cls_name = val['__class__']
                if cls_name in classes:
                    self.__objects[key] = classes[cls_name](**val)

    def delete(self, obj=None):
        """Deletes an object from storage."""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
                self.save()
