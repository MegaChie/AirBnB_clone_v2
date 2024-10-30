#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import shlex
import json
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Review": Review
}


class HBNBCommand(cmd.Cmd):
    """
    Contains functionality for the HBNB console

    Attributes:
        prompt (str):       prompt for console
        dot_cmds (list):    list of commands that require dot notation
        types (dict):       dictionary of types for casting
    """
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int,
        'number_bathrooms': int,
        'max_guest': int,
        'price_by_night': int,
        'latitude': float,
        'longitude': float
    }

    def parse_pairs(self, args):
        """
        Parses key-value pairs

        Args:
            args (str):         string to parse

        Returns:
            parsed_dict (dict): dictionary of key-value pairs
        """
        parsed_dict = {}
        for pair in args:
            if "=" in pair:
                key, value = pair.split("=", 1)
                parsed_dict[key] = value.strip('"')
        return parsed_dict

    def do_quit(self, command):
        """Exits the HBNB console"""
        return True

    def do_exit(self, command):
        """Exits the HBNB console"""
        return True

    def do_EOF(self, arg):
        """Handles EOF to exit program without formatting"""
        print()
        return True

    def do_create(self, args):
        """Creates an object that inherits from BaseModel"""
        split_args = shlex.split(args)
        if len(split_args) == 0:
            print("** class name missing **")
            return
        class_name = split_args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return

        new_obj = classes[class_name]()  # create new object
        parsed_pairs = self.parse_pairs(split_args[1:])

        for key, value in parsed_pairs.items():
            if hasattr(new_obj, key):
                if key in ["name", "description"]:
                    value = value.replace('_', ' ')
                setattr(new_obj, key, value)

        new_obj.save()

    def do_show(self, args):
        """Shows an individual object"""
        split_args = args.split()
        if len(split_args) == 0:
            print("** class name missing **")
            return
        if len(split_args) == 1:
            print("** instance id missing **")
            return
        cls_name, obj_id = split_args[0], split_args[1]

        if cls_name not in classes:
            print("** class doesn't exist **")
            return

        obj_dict = storage.all(cls_name)
        key = f"{cls_name}.{obj_id}"

        if key not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict[key])

    def do_destroy(self, args):
        """Destroys a specified object"""
        split_args = args.split()
        if len(split_args) == 0:
            print("** class name missing **")
            return
        if len(split_args) == 1:
            print("** instance id missing **")
            return

        cls_name, obj_id = split_args[0], split_args[1]
        if cls_name not in classes:
            print("** class doesn't exist **")
            return

        obj_dict = storage.all(classes[cls_name])
        key = f"{cls_name}.{obj_id}"

        if key not in obj_dict:
            print("** no instance found **")
        else:
            storage.delete(obj_dict[key])
            storage.save()
            print(f"{obj_id} deleted")

    def do_resetdb(self, args):
        """Destroys all models in the database, completely emptying it."""
        if input("Are you sure you want to delete everything in the database?\
                  This cannot be undone. [y/N]: ").lower() == "y":
            size = len(storage.all())
            for model in list(storage.all().values()):
                model.delete()
            print(f"Database reset. {size