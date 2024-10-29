#!/usr/bin/python3
""" Console Module """
import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State

class HBNBCommand(cmd.Cmd):
    """ HBNB console """
    prompt = '(hbnb) '

    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'City': City,
        'Amenity': Amenity,
        'Review': Review,
        'State': State
    }

    # commands for console

    # create class
    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.classes[class_name]()
        for param in args[1:]:
            key_value = param.split("=")
            if len(key_value) == 2:
                key, value = key_value
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                setattr(new_instance, key, value)
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """ Show an instance based on class name and id """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = f"{class_name}.{instance_id}"
        instance = storage.all().get(key)
        if not instance:
            print("** no instance found **")
            return
        print(instance)

    def do_all(self, arg):
        """ Show all instances of a class """
        args = arg.split()
        # if its not in args then show all
        if not args:
            instances = storage.all()
        else:
            # if is in args show all that class
            class_name = args[0]
            if class_name not in globals():
                print("** class doesn't exist **")
                return
            instances = storage.all(globals()[class_name])
        # print instances
        for instance in instances.values():
            print(instance)

    def do_destroy(self, arg):
        """ Destroy an instance based on class name and id """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = f"{class_name}.{instance_id}"
        instance = storage.all().get(key)
        if not instance:
            print("** no instance found **")
            return
        storage.delete(instance)
        storage.save()

    def do_update(self, arg):
        """ Update an instance based on class name and id """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = f"{class_name}.{instance_id}"
        instance = storage.all().get(key)
        if not instance:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3].strip('"').replace('_', ' ')
        setattr(instance, attr_name, attr_value)
        instance.save()

    def do_EOF(self, arg):
        """ Handle EOF to exit the console """
        print()
        return True

    def do_quit(self, arg):
        """ Handle quit to exit the console """
        return True

if __name__ == '__main__':
    HBNBCommand().cmdloop()
