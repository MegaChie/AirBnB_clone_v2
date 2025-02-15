#!/usr/bin/python3
"""file storage for AirBnB project"""

from models.user import User
from models.place import Place
from models.review import Review
from models.city import City
from models.amenity import Amenity
from models.base_model import BaseModel
import shlex
from models.state import State
import json


class FileStorage:
    """serializes instances to a JSON and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """

    __file_path = "file.json"  # path to the JSON file
    __objects = {}  # Dictionary to store objects

    def all(self, cls=None):
        """
        Return:
            returns dictionary of __object
        """
        if cls is None:
            return self.__objects
        else:
            return {
                    key: obj for key,
                    obj in self.__objects.items() if isinstance(obj, cls)
                    }

    def new(self, obj):
        """sets __object given obj
        Args:
            obj: given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """serialize the file path to JSON
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ delete existing element
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """the calls will reload()
        """
        self.reload()
