#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import importlib


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        classes = {'BaseModel',
                'User', 'Place',
                'State', 'City', 'Amenity',
                'Review'
              }
        
        if cls is not None:
            if isinstance(cls, str):
                if cls not in classes:
                    return {}
                try:
                    # Dynamically import the class
                    module_path = f"models.{cls.lower()}"  # Convert class name to module name
                    module = importlib.import_module(module_path)
                    cls = getattr(module, cls)  # Get the class from the module
                    
                except (ImportError, AttributeError):
                    print("** class doesn't exist **")
                
                    
            # Filter objects based on the class
            return {
                key: value
                for key, value in self.__objects.items()
                if isinstance(value, cls)
                }
                
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w', encoding='utf-8') as outfile:
            temp = {
                key: value.to_dict()
                for key, value in self.__objects.items()
                }
            
            json.dump(temp, outfile)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete object from storage."""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
                self.save()
