#!/usr/bin/env python3
""" Module for FileStorage class, which handles storage of object data in JSON format. """

import json
import os
import models
from models.base_model import BaseModel

class FileStorage:
    """ This class manages storage of model instances in JSON format. """
    
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ 
        Returns a dictionary of all objects or objects of a specific class.

        Args:
            cls (type): The class to filter objects by. If None, returns all objects.

        Returns:
            dict: A dictionary of objects.
        """
        if cls is None:
            return FileStorage.__objects
        return {key: obj for key, obj in FileStorage.__objects.items() if isinstance(obj, cls)}

    def new(self, obj):
        """ 
        Adds a new object to the storage.

        Args:
            obj (BaseModel): The object to add.
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """ 
        Saves the current state of objects to a JSON file.
        """
        with open(FileStorage.__file_path, 'w') as f:
            json.dump({key: obj.to_dict() for key, obj in FileStorage.__objects.items()}, f)

    def delete(self, obj=None):
        """ 
        Deletes an object from storage.

        Args:
            obj (BaseModel, optional): The object to delete. If None, does nothing.
        """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def reload(self):
        """Deserialize the JSON file to __objects."""
        if os.path.exists(self.__file_path):
            try:
                with open(self.__file_path, 'r', encoding='utf-8') as f:
                    obj_dict = json.load(f)
                    for key, value in obj_dict.items():
                        if '__class__' in value:
                            cls_name = value['__class__']
                            cls = models.classes[cls_name]
                            self.__objects[key] = cls(**value)
                        else:
                            print(f"Warning: Missing '__class__' key in {key}")
            except json.JSONDecodeError:
                # Handle the case where the JSON file is empty or malformed
                print(f"Warning: The file {self.__file_path} is empty or malformed.")
