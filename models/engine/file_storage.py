#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""

import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            clsDict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    clsDict[key] = value
            return clsDict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
         with open(self.__file_path, "r") as f:
                od = json.load(f)
                for obj in od.values():
                    clsName = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(clsName)(**obj))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists"""
        if obj:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def clear(self):
        """Clear all objects from storage"""
        self.__objects.clear()
        
