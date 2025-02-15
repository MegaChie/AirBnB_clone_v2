#!/usr/bin/python3
"""Console Module."""
import cmd
import ast
import sys
import re
import json
import sqlalchemy
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    def preloop(self):
        """Print if isatty is false."""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        # substitute single quote for double to handle json parsing
        line = re.sub(r'[\']', '"', line[:])

        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not all(char in line for char in {'.', '(', ')'}):
            #         if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            parsed_line = line[:]  # parsed line

            # isolate <class name>
            _cls = parsed_line[:parsed_line.find('.')]

            # isolate and validate <command>
            _cmd = parsed_line[parsed_line.find('.') + 1:parsed_line.find('(')]

            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            args = parsed_line[parsed_line.find('(') + 1:parsed_line.find(')')]
            if args:
                # partition args: (<id>, [<delim>], [<*args>])
                _id, _, attr_name_and_value = args.partition(', ')
#                 pline = pline.partition(', ')  # pline convert to tuple

                # strip leading quotes and spaces
                _id = _id.strip('\'" ')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # strip leading quotes and spaces
                attr_name_and_value = attr_name_and_value.strip('\'" ')

                # if arguments exist beyond _id
                if attr_name_and_value:
                    # check for *args or **kwargs
                    if attr_name_and_value.startswith("{") or\
                       attr_name_and_value.endswith("}"):
                        _args = attr_name_and_value
                    else:
                        _args = attr_name_and_value.replace(',', '')

            line = ' '.join([_cmd, _cls, _id, _args])
        except Exception as mess:
            pass

        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false."""
        if not sys.__stdin__.isatty() and line.strip() != "":
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, line):
        """Method to exit the HBNB console."""
        return True

    def help_quit(self):
        """Prints the help documentation for quit."""
        print("Exits the program with formatting\n")

    def do_EOF(self, line):
        """Handles EOF to exit program."""
        return True

    def help_EOF(self):
        """Prints the help documentation for EOF."""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD."""
        pass

    def do_create(self, args):
        """Create an object of any class."""
        cls, _, params = args.partition(" ")

        if not cls:
            print("** class name missing **")
            return

        if cls not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        new_instance = HBNBCommand.classes[cls]()

        if params:
            strings = r"""["'](?P<string>[A-Za-z0-9_,!@#$%^&*\.-]+)["']"""
            floats = r"(?P<float>(?:[-]?[0-9]+(?=\.))(?:\.[0-9]*(?![\.0-9-]+))"
            ints = r"(?P<int>[-]?[0-9]+(?=\s))"

            # pattern for param syntax:
            # <key name>=<value> [<key name>=<value>...]
            attr_pattern = rf"""
            \b(?P<attr_name>[A-Za-z_]+)(?=\=)                  # Attribute name
            (?:\=)
            (?P<value>{strings}|(?P<numeric>{ints}|{floats}))) # Attr value
            (?:\s*)
            """
            pattern = re.compile(attr_pattern, re.VERBOSE)
            matches = pattern.findall(params)

            if matches:
                attr_dict = {}
                for match in matches:
                    key, value, str_val, num_val, _, _ = match
                    try:
                        val = json.loads(
                            value) if str_val else json.loads(num_val)

                    except (SyntaxError, json.JSONDecodeError) as e:
                        pass

                    else:
                        if isinstance(val, str) and '_' in val:
                            translator = str.maketrans("_", " ")
                            attr_dict[key] = val.translate(translator)
                        else:
                            attr_dict[key] = val

                new_instance = HBNBCommand.classes[cls](**attr_dict)

        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """Help information for the create method."""
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")
        print("[Usage]: create <className> <key name>=<value>" +
              " [<key name>=<value>...]\n")

    def do_show(self, line):
        """Method to show an individual object."""
        cls, _, instance_id = line.partition(" ")

        if not cls:
            print("** class name missing **")
            return

        if cls not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not instance_id:
            print("** instance id missing **")
            return

        instance_id = instance_id.strip('\'" ')

        key = f"{cls}.{instance_id}"

        if key not in storage.all().keys():
            print("** no instance found **")
            return

        print(storage.all()[key])

    def help_show(self):
        """Help information for the show command."""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, line):
        """Destroy a specified object."""
        cls, _, instance_id = line.partition(" ")

        if not cls:
            print("** class name missing **")
            return

        if cls not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not instance_id:
            print("** instance id missing **")
            return

        instance_id = instance_id.strip('\'" ')

        key = f"{cls}.{instance_id}"

        if key not in storage.all().keys():
            print("** no instance found **")
            return

        storage.delete(storage.all().copy()[key])

    def help_destroy(self):
        """Help information for the destroy command."""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Show all objects, or all objects of a class."""
        print_list = []

        if args:
            cls = args.split(' ')[0]  # remove possible trailing args

            if cls not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            for key, value in storage.all().items():
                if key.split('.')[0] == cls:
                    print_list.append(str(value))
        else:
            for key, value in storage.all().items():
                print_list.append(str(value))

        print(print_list)

    def help_all(self):
        """Help information for the all command."""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, line):
        """Count current number of class instances."""

        cls, _, _ = line.partition(" ")

        if not cls:
            print("** class name missing **")
            return

        if cls not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        count = 0
        for key in storage.all():
            if cls == key.split('.')[0]:
                count += 1

        print(count)

    def help_count(self):
        """Help information for the count command."""
        print("Usage: count <class_name>")

    def do_update(self, line):
        """Update a certain object with new info."""
        # isolate cls from id/args
        cls, _, args = line.strip().partition(" ")

        if not cls:
            print("** class name missing **")
            return

        if cls not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        instance_id, _, args_or_kwargs = args.strip().partition(" ")
        instance_id = instance_id.strip("\"' ")
        args_or_kwargs = args_or_kwargs.strip("\"' ")

        if not instance_id:
            print("** instance id missing **")
            return

        # generate key from class and id
        key = f"{cls}.{instance_id}"

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # Retrieve object to update its attributes
        updated_obj = storage.all()[key]

        if args_or_kwargs:
            if any(char in args_or_kwargs for char in '{}'):
                # Handle dictionary representation
                try:
                    # Safely evaluates Python dictionary-like strings
                    attr_dict = ast.literal_eval(args_or_kwargs.strip("\"' "))
                    if not isinstance(attr_dict, dict):
                        raise ValueError
                except (SyntaxError, ValueError):
                    print("** invalid dictionary representation **")
                    return
                else:
                    for attr_name, attr_value in attr_dict.items():
                        attr_name = attr_name.strip("\"' ")

                        if isinstance(attr_value, str):
                            attr_value = attr_value.strip("\"' ")

                        setattr(updated_obj, attr_name, attr_value)

            else:
                attr_name, _, attr_value = args_or_kwargs.partition(" ")

                if not attr_value:
                    print("** value missing **")
                    return

                attr_name = attr_name.strip("\"' ")

                attr_value = attr_value.strip("\"' ")

                # guard against trailing args
                attr_value, _, xtra_args = attr_value.partition(" ")

                attr_value = attr_value.strip("\"' ")

                if not xtra_args:
                    try:
                        # Convert to appropriate type if possible
                        attr_value = json.loads(attr_value)
                    except (json.JSONDecodeError):
                        pass  # Keep as string if evaluation fails
                    except Exception as e:
                        pass
                    finally:
                        setattr(updated_obj, attr_name, attr_value)

        else:
            print("** attribute name missing **")
            return

        updated_obj.save()  # Save the updated object

    def help_update(self):
        """Help information for the update class."""
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
