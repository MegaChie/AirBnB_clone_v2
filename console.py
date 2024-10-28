#!/usr/bin/python3
""" Console Module """
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """ HBNB console """
    prompt = '(hbnb) '

    def do_create(self, arg):
        """ Create a new instance of a class """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        new_instance = globals()[class_name]()
        for param in args[1:]:
            key, value = param.split('=')
            setattr(new_instance, key, value.strip('"').replace('_', ' '))
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
        if not args:
            instances = storage.all()
        else:
            class_name = args[0]
            if class_name not in globals():
                print("** class doesn't exist **")
                return
            instances = storage.all(globals()[class_name])
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
