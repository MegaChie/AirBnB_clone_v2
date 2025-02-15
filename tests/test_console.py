#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unittest suites for the HBNBCommand class for FileStorage and DBStorage.
"""
import os
import time
import unittest
import MySQLdb
from sqlalchemy.exc import IntegrityError
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine.db_storage import DBStorage
from tests.test_models.test_engine.test_db_storage import BaseTestDBStorage


__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-02-11"
__version__ = "2.1"


class TestBuiltInConsoleCommands(unittest.TestCase):
    """Test cases for the HBNBCommand class."""

    def test_quit_command(self):
        """Test the quit command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_eof_command(self):
        """Test the EOF command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_empty_line(self):
        """Test empty line input."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))

    def test_help_command(self):
        """Test the help command."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("help")
            self.assertIn("Documented commands", output.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_line(self, mock_stdout):
        """Test that empty line does nothing."""
        # Simulate pressing ENTER with an empty line
        HBNBCommand().onecmd("")
        self.assertEqual(mock_stdout.getvalue(), "")  # No output expected

    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_line_with_spaces(self, mock_stdout):
        """Test that a line with only spaces does nothing."""
        # Simulate pressing ENTER with a line of spaces
        HBNBCommand().onecmd("   ")
        self.assertEqual(mock_stdout.getvalue(), "")  # No output expected


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Skipping: not using DBStorage")
class TestFileStorageConsole(unittest.TestCase):
    _classes = {'BaseModel',
                'User',
                'Place',
                'State',
                'City',
                'Amenity',
                'Review'
                }

    @classmethod
    def setUpClass(cls):
        """Set up the test environment by creating a FileStorage instance and
        clearing the file."""
        cls.file_path = "file.json"
        cls.storage = storage
        cls.storage.reload()  # Ensure the database session is reloaded
        cls.storage._FileStorage__objects.clear()

    @classmethod
    def tearDownClass(cls):
        """Clean up after each test by removing the test file."""
        if os.path.exists(cls.file_path):
            os.remove(cls.file_path)

    def setUp(self):
        """Set up test environment"""
        self.storage.reload()

    def tearDown(self):
        """Clean up after each test"""
        # Clear the in-memory cache of objects
        self.storage.all().clear()


class TestCreateCommand(TestFileStorageConsole):
    """Test cases for the create command."""

    def test_create_each_class_without_kwargs(self):
        """Test create command for each class."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                self.assertRegex(instance_id,
                                 r'^[0-9a-f-]{36}$')
                key = cls + "." + instance_id
                print(key)
                self.assertIn(key, self.storage.all())

    def test_create_invalid_class(self):
        """Test create with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("create FakeClass")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_storage_entries_count(self):
        """Test Number of record in storage for each class."""
        self.assertEqual(len(self.storage.all()), len(self._classes))

        for model in self._classes:
            if model != "BaseModel":
                self.assertEqual(len(self.storage.all(model)), 1)


class TestShowCommand(TestFileStorageConsole):
    """Test cases for the show command."""

    def test_show_valid_instance(self):
        """Test show with a valid instance."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as show_output:
                    HBNBCommand().onecmd(f"show {cls} {instance_id}")
                    self.assertIn(instance_id, show_output.getvalue().strip())

    def test_show_invalid_class(self):
        """Test show with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("show FakeClass 1234")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_show_missing_id(self):
        """Test show with a missing ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"show {cls}")
                self.assertEqual(output.getvalue().strip(),
                                 "** instance id missing **")

    def test_show_nonexistent_id(self):
        """Test show with a nonexistent ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"show {cls} 1234")
                self.assertEqual(output.getvalue().strip(),
                                 "** no instance found **")


class TestUpdateCommand(TestFileStorageConsole):
    """Test cases for the show command."""

    def test_update_valid_instance(self):
        """Test update command for each class."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as update_output:
                    HBNBCommand().onecmd(
                        f"update {cls} {instance_id} author 'Albert'")
                    self.assertEqual(update_output.getvalue().strip(), "")

    def test_update_invalid_class(self):
        """Test show with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("update FakeClass 1234 author 'Albert'")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_update_nonexistent_id(self):
        """Test show with a nonexistent ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                with patch('sys.stdout', new=StringIO()) as update_output:
                    HBNBCommand().onecmd(f"update {cls} 1234 author 'Albert'")
                    self.assertEqual(update_output.getvalue().strip(),
                                     "** no instance found **")

    def test_update_missing_id(self):
        """Test show with a missing ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"update {cls}")
                self.assertEqual(output.getvalue().strip(),
                                 "** instance id missing **")

    def test_update_missing_attr_name(self):
        """Test show with a missing ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as update_output:
                    HBNBCommand().onecmd(
                        f"update {cls} {instance_id}")
                self.assertEqual(update_output.getvalue().strip(),
                                 "** attribute name missing **")

    def test_update_missing_attr_value(self):
        """Test show with a missing ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as update_output:
                    HBNBCommand().onecmd(f"update {cls} {instance_id} author")
                    self.assertEqual(update_output.getvalue().strip(),
                                     "** value missing **")


class TestDestroyCommand(TestFileStorageConsole):
    """Test cases for the destroy command."""

    def test_destroy_valid_instance(self):
        """Test destroy with a valid instance."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()
                with patch('sys.stdout', new=StringIO()) as destroy_output:
                    HBNBCommand().onecmd(f"destroy {cls} {instance_id}")
                    self.assertEqual(destroy_output.getvalue().strip(), "")

    def test_destroy_invalid_class(self):
        """Test destroy with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("destroy FakeClass 1234")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_destroy_missing_id(self):
        """Test destroy with a missing ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"destroy {cls}")
                self.assertEqual(output.getvalue().strip(),
                                 "** instance id missing **")

    def test_destroy_nonexistent_id(self):
        """Test destroy with a nonexistent ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                with patch('sys.stdout', new=StringIO()) as destroy_output:
                    HBNBCommand().onecmd(f"destroy {cls} 1234")
                    self.assertEqual(destroy_output.getvalue().strip(),
                                     "** no instance found **")


class TestAllCommand(TestFileStorageConsole):
    """Test cases for the all command."""

    def setUp(self):
        """Set up the test environment by creating a FileStorage instance and
        clearing the file."""
        self.storage.reload()

        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")

    def test_all(self):
        """Test all command without class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("all")
            self.assertIsInstance(output.getvalue().strip(), str)

    def test_all_with_class(self):
        """Test all command with a valid class."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"all {cls}")
                self.assertIsInstance(output.getvalue().strip(), str)

    def test_all_invalid_class(self):
        """Test all command with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("all FakeClass")
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")


class TestDotCommands(TestFileStorageConsole):
    """Test cases for count, show, and update commands for each class."""

    def setUp(self):
        """Set up the test environment by creating a FileStorage instance and
        clearing the file."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")

    def test_count(self):
        """Test count command for each class."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as count_output:
                command = HBNBCommand().precmd(
                    f"{cls}.count()")  # Manually process command
                HBNBCommand().onecmd(command)  # Execute transformed command
                self.assertRegex(count_output.getvalue().strip(), r'^\d+$')

    def test_show_nonexistent(self):
        """Test show command with nonexistent ID for each class."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as show_output:
                command = HBNBCommand().precmd(
                    f"{cls}.show(1234)")  # Manually process command
                HBNBCommand().onecmd(command)  # Execute transformed command
                self.assertEqual(show_output.getvalue().strip(),
                                 "** no instance found **")

    def test_all(self):
        """Test all command without class."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                command = HBNBCommand().precmd(
                    f"{cls}.all()")  # Manually process command
                HBNBCommand().onecmd(command)
                self.assertIsInstance(output.getvalue().strip(), str)
                self.assertNotEqual(len(output.getvalue().strip()), len('[]'))
                self.assertTrue(output.getvalue().strip().startswith("[")
                                and
                                output.getvalue().strip().endswith("]"))

        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()

                all_instance_entry = f"[{cls}] ({instance_id})"

                with patch('sys.stdout', new=StringIO()) as all_output:
                    command = HBNBCommand().precmd(
                        f"{cls}.all()")  # Manually process command

                    # Execute transformed command
                    HBNBCommand().onecmd(command)
                    self.assertIn(all_instance_entry,
                                  all_output.getvalue().strip())

        # clear storage and remove json file to test for empty storage call
        self.tearDown()
        self.tearDownClass()

        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                command = HBNBCommand().precmd(
                    f"{cls}.all()")  # Manually process command
                HBNBCommand().onecmd(command)

                self.assertEqual(output.getvalue().strip(), '[]')
                self.assertTrue(len(output.getvalue().strip()), 2)

    def test_all_invalid_class(self):
        """Test all command with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            # Manually process command
            command = HBNBCommand().precmd("FakeClass.all()")
            HBNBCommand().onecmd(command)  # Execute transformed command
            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_update(self):
        """Test update command for each class."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()

                with patch('sys.stdout', new=StringIO()) as update_output:
                    command = HBNBCommand().precmd(
                        f"{cls}.update({instance_id}, attr_name, 'value')")
                    HBNBCommand().onecmd(command)

                    self.assertEqual(update_output.getvalue().strip(), "")

                with patch('sys.stdout', new=StringIO()) as all_output:
                    command = HBNBCommand().precmd(
                        f"{cls}.all()")  # Manually process command

                    # Execute transformed command
                    HBNBCommand().onecmd(command)
                    self.assertTrue(all(item in all_output.getvalue().strip()
                                    for item in ('attr_name', 'value')))

    def test_update_nonexistent(self):
        """Test update command with nonexistent ID for each class."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as update_output:
                command = HBNBCommand().precmd(
                    f"{cls}.update(1234, attr_name, 'value')")
                HBNBCommand().onecmd(command)
                self.assertEqual(update_output.getvalue().strip(),
                                 "** no instance found **")

    def test_destroy_valid_instance(self):
        """Test destroy with a valid instance."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()

                with patch('sys.stdout', new=StringIO()) as destroy_output:
                    command = HBNBCommand().precmd(
                        f"{cls}.destroy({instance_id})")
                    HBNBCommand().onecmd(command)

                    self.assertEqual(destroy_output.getvalue().strip(), "")

    def test_destroy_invalid_class(self):
        """Test destroy with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as output:
            command = HBNBCommand().precmd("FakeClass.destroy(1234)")
            HBNBCommand().onecmd(command)

            self.assertEqual(output.getvalue().strip(),
                             "** class doesn't exist **")

    def test_destroy_missing_id(self):
        """Test destroy with a missing ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                command = HBNBCommand().precmd(f"{cls}.destroy()")
                HBNBCommand().onecmd(command)

                self.assertEqual(output.getvalue().strip(),
                                 "** instance id missing **")

    def test_destroy_nonexistent_id(self):
        """Test destroy with a nonexistent ID."""
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as destroy_output:
                command = HBNBCommand().precmd(f"{cls}.destroy(1234)")
                HBNBCommand().onecmd(command)

                self.assertEqual(destroy_output.getvalue().strip(),
                                 "** no instance found **")


class TestShowUpdateCommandsWithDict(TestFileStorageConsole):
    """Test cases for show and update commands with dictionary input for each
    class."""

    def test_show_with_dict(self):
        """
        Test show command when a dictionary is used in update for each class.
        """
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                instance_id = output.getvalue().strip()

                with patch('sys.stdout', new=StringIO()) as update_output:
                    command = HBNBCommand().precmd(
                        f"{cls}.update({instance_id}, {{'author': 'Albert'}})")
                    HBNBCommand().onecmd(command)
                    self.assertEqual(update_output.getvalue().strip(), "")

                with patch('sys.stdout', new=StringIO()) as show_output:
                    command = HBNBCommand().precmd(
                        f"{cls}.show({instance_id})")
                    HBNBCommand().onecmd(command)
                    self.assertIn("'author': 'Albert'",
                                  show_output.getvalue().strip())

    def test_update_with_dict_nonexistent_id(self):
        """
        Test update command with dictionary for nonexistent ID in each class.
        """
        for cls in self._classes:
            with patch('sys.stdout', new=StringIO()) as output:
                command = HBNBCommand().precmd(
                    f"{cls}.update(1234, {{'author': 'Albert'}})")
                HBNBCommand().onecmd(command)

                self.assertEqual(output.getvalue().strip(),
                                 "** no instance found **")


class TestDBStorageConsole(BaseTestDBStorage):

    DB_CLASSES = {'users': User,
                  'places': Place,
                  'states': State,
                  'cities': City,
                  'amenities': Amenity,
                  'reviews': Review
                  }

    @classmethod
    def get_model_class(cls, tablename):
        """Get the model class for a given table name"""
        return cls.DB_CLASSES.get(tablename)

    @classmethod
    def create_attr_for_entries_created_based_table_name(cls, tablename):
        """Get the model class for a given table name"""
        setattr(cls, tablename, [])

    def test_01_DBStorage__object_has_no_object_of_the_model(self):
        """Confirm __objects is empty"""
        self.assertEqual(len(self.storage.all(self.model)), 0)

    def test_02_table_is_empty(self):
        """Confirm table is empty"""
        self.assertEqual(self.get_table_entries_count(), 0)

    def test_04_DBStorage__objects_not_empty_and_has_one_object(self):
        """Confirm __objects is not empty"""
        entries = getattr(self, self.tablename)

        self.assertTrue(len(self.storage.all(self.model)) > 0)
        self.assertEqual(len(self.storage.all(self.model)),
                         self.get_table_entries_count())
        self.assertEqual(len(self.storage.all(self.model)), len(entries))
        self.assertEqual(len(self.storage.all(self.model)), 1)
        self.assertEqual(len(entries), 1)
        self.assertEqual(self.get_table_entries_count(), 1)
        self.assertIn(entries[-1], self.storage.all(self.model).keys())

    def test_05_table_is_not_empty_and_has_one_entry(self):
        """Confirm the model's table is not empty"""
        entries = getattr(self, self.tablename)

        self.assertTrue(self.get_table_entries_count() >
                        0, "Entry was not added to DB")
        self.assertEqual(len(self.storage.all(self.model)),
                         self.get_table_entries_count())
        self.assertEqual(len(self.storage.all(self.model)), len(entries))
        self.assertEqual(self.get_table_entries_count(), len(entries))
        self.assertEqual(len(self.storage.all(self.model)), 1)
        self.assertEqual(len(entries), 1)
        self.assertEqual(self.get_table_entries_count(), 1)

    def test_07_DBStorage__objects_has_two_objects_of_the_model(self):
        """Confirm __objects size is greater thant 1"""
        # update table entries count
        entries = getattr(self, self.tablename)

        self.assertTrue(len(self.storage.all(self.model))
                        > 1, "Entry was not added to DB")
        self.assertEqual(len(self.storage.all(self.model)),
                         len(entries), "Entry was not added to DB")
        self.assertEqual(len(self.storage.all(self.model)),
                         self.get_table_entries_count())
        self.assertIn(entries[-1], self.storage.all(self.model).keys())
        self.assertEqual(len(self.storage.all(self.model)), 2)
        self.assertEqual(len(entries), 2)
        self.assertEqual(self.get_table_entries_count(), 2)

    def test_08_table_has_two_entries(self):
        """Confirm users table has more than one row"""
        entries = getattr(self, self.tablename)

        self.assertTrue(self.get_table_entries_count() >
                        1, "Entry was not added to DB")
        self.assertEqual(self.get_table_entries_count(),
                         len(entries), "Entry was not added to DB")
        self.assertEqual(len(self.storage.all(self.model)),
                         self.get_table_entries_count())
        self.assertEqual(self.get_table_entries_count(), len(entries))
        self.assertEqual(len(self.storage.all(self.model)), 2)
        self.assertEqual(len(entries), 2)
        self.assertEqual(self.get_table_entries_count(), 2)

    def test_09_deletion_of_last_table_entry(self):
        """Cleanup: Delete the last created table entry from the database"""
        entries = getattr(self, self.tablename)
        initial_count = len(entries)

        self.assertEqual(self.get_table_entries_count(), initial_count)
        self.assertEqual(len(self.storage.all(self.model)),
                         self.get_table_entries_count())
        self.assertEqual(self.get_table_entries_count(), initial_count)
        self.assertEqual(len(self.storage.all(self.model)), 2)
        self.assertEqual(len(entries), 2)
        self.assertEqual(self.get_table_entries_count(), 2)

        key = entries[-1]

        self.storage.delete(storage.all(self.model)[key])

        entry_id = key.split('.')[-1]

        # Refresh the MySQLdb connection to see the changes
        self.conn.commit()

        entries.pop(-1)

        self.assertTrue(len(self.users) < initial_count,
                        "Entry not deleted from the DB")
        self.assertEqual(self.get_table_entries_count(),
                         initial_count-1, "Entry not deleted from the DB")
        self.assertEqual(len(self.storage.all(self.model)),
                         self.get_table_entries_count(),
                         "Entry not deleted from the DB")
        self.assertEqual(len(self.storage.all(self.model)),
                         initial_count-1, "Entry not deleted from the DB")
        self.assertEqual(len(entries),
                         self.get_table_entries_count(),
                         "Entry not deleted from the DB")
        self.assertEqual(len(self.storage.all(self.model)), len(
            entries), "Entry not deleted from the DB")
        self.assertEqual(len(self.storage.all(self.model)), 1)
        self.assertEqual(len(entries), 1)
        self.assertEqual(self.get_table_entries_count(), 1)

        query = f"SELECT * FROM {self.tablename} WHERE id=%s"
        self.cursor.execute(query, (entry_id,))
        result = self.cursor.fetchone()
        self.assertTrue(result is None)

    def test_10_only_one_entry_exists_after_last_deletion(self):
        """Helper function to count records in users table"""
        query = f"SELECT * FROM {self.tablename}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        self.assertTrue(result is not None)

    def test_11_create_a_table_entry_without_kwargs(self):
        """Test that creating a record with missing attributes via the console
        does not add it to the database"""
        models = {'users': "User",
                  'places': "Place",
                  'states': "State",
                  'cities': "City",
                  'amenities': "Amenity",
                  'reviews': "Review"
                  }

        with patch("sys.stdout", new=StringIO()) as output:
            args = f'create {models[self.tablename]}'
            HBNBCommand().onecmd(args)
            instance_id = output.getvalue().strip()

        self.assertEqual(instance_id, "")
        self.assertFalse(instance_id)


class Test_02_User(TestDBStorageConsole):
    """Tests DBStorage integration with console commands for the User model"""
    tablename = "users"

    model = TestDBStorageConsole.get_model_class(tablename)

    TestDBStorageConsole.create_attr_for_entries_created_based_table_name(
        tablename)

    def test_03_create_user_all_valid_attributes(self):
        """Test that creating a User via the console adds it to the database"""
        # Capture console output
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd(
                'create User email="gui@hbtn.io" password="guipwd" ' +
                'first_name="Guillaume" last_name="Snow"')
            user_id = output.getvalue().strip()

        self.assertNotEqual(user_id, "",
                            "Failed to get User ID from console output")
        self.assertTrue(len(user_id) > 0,
                        "Failed to get User ID from console output")
        self.assertRegex(user_id, r'^[0-9a-f-]{36}$')
        self.users.append("User." + user_id)

    def test_06_create_user_missing_nullable_attributes(self):
        """Test that creating a User with missing nullable attributes via the
        console does not add it to the database"""
        # Test user creation missing last_name & first_name attributes
        with patch("sys.stdout", new=StringIO()) as output:
            args = 'create User email="a@a.com" password="pwd"'
            HBNBCommand().onecmd(args)

            user_id = output.getvalue().strip()

        self.assertNotEqual(user_id, "",
                            "Failed to get User ID from console output")
        self.assertTrue(len(user_id) > 0,
                        "Failed to get User ID from console output")
        self.assertRegex(user_id, r'^[0-9a-f-]{36}$')
        self.users.append("User." + user_id)

    def test_13_create_user_missing_non_nullable_attributes(self):
        """
        Test that creating a User via the console with missing non_nullable
        attributes does not add it to the database
        """
        # Test missing email and password attributes
        with patch("sys.stdout", new=StringIO()) as output:
            args = 'create User first_name="Guillaume" last_name="Snow"'
            HBNBCommand().onecmd(args)
            user_id = output.getvalue().strip()

        self.assertEqual(user_id, "")
        self.assertFalse(user_id)

        # Test missing password attribute
        with patch("sys.stdout", new=StringIO()) as output:
            args = 'create User email="a@a.com"'
            HBNBCommand().onecmd(args)
            user_id = output.getvalue().strip()

        self.assertEqual(user_id, "")
        self.assertFalse(user_id)

        # Test missing email attribute
        with patch("sys.stdout", new=StringIO()) as output:
            args = 'create User password="pwd"'
            HBNBCommand().onecmd(args)
            user_id = output.getvalue().strip()

        self.assertEqual(user_id, "")
        self.assertFalse(user_id)


class Test_03_State(TestDBStorageConsole):
    """
    Tests DBStorage integration with console commands for the State model
    """
    tablename = "states"

    model = TestDBStorageConsole.get_model_class(tablename)

    TestDBStorageConsole.create_attr_for_entries_created_based_table_name(
        tablename)

    def test_03_create_state_valid_attributes(self):
        """Test that creating a User via the console adds it to the database"""
        # Capture console output
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="California"')
            state_id = output.getvalue().strip()

        self.assertNotEqual(state_id, "",
                            "Failed to get State ID from console output")
        self.assertTrue(len(state_id) > 0,
                        "Failed to get State ID from console output")
        self.assertRegex(state_id, r'^[0-9a-f-]{36}$')
        self.states.append("State." + state_id)

    def test_06_create_additional_state_with_valid_attributes(self):
        """Test that creating a User via the console adds it to the database"""
        # Capture console output
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="Nevada"')
            state_id = output.getvalue().strip()

        self.assertNotEqual(state_id, "",
                            "Failed to get State ID from console output")
        self.assertTrue(len(state_id) > 0,
                        "Failed to get State ID from console output")
        self.assertRegex(state_id, r'^[0-9a-f-]{36}$')
        self.states.append("State." + state_id)


class Test_04_City(TestDBStorageConsole):
    """
    Tests DBStorage integration with console commands for the City model
    """
    tablename = "cities"

    model = TestDBStorageConsole.get_model_class(tablename)

    TestDBStorageConsole.create_attr_for_entries_created_based_table_name(
        tablename)

    def test_03_create_city_existing_state_id(self):
        """
        Test that creating a City via the console adds it to the database
        """

        self.assertNotEqual(self.get_table_entries_count(
            "states"), 0, "states table is empty")
        self.assertTrue(self.get_table_entries_count(
            "states") >= 1, "states table is empty")

        # 1. Get a valid state_id from and existing state
        query = "SELECT id from states;"
        self.cursor.execute(query)
        state_id = self.cursor.fetchone()[0]

        # Create city from an existing state
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create City name="San_Francisco" state_id="{state_id}"'
            HBNBCommand().onecmd(arg)
            city_id = output.getvalue().strip()

        self.assertNotEqual(city_id, "",
                            "Failed to get City ID from console output")
        self.assertTrue(len(city_id) > 0,
                        "Failed to get City ID from console output")
        self.assertRegex(city_id, r'^[0-9a-f-]{36}$')
        self.cities.append("City." + city_id)

    def test_06_create_city_all_existing_attributes(self):
        """
        Test that creating a City via the console adds it to the database
        """
        initial_state_count = self.get_table_entries_count("states")

        # 1. Create a new State first since City requires a valid state_id
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="Nevada"')
            state_id = output.getvalue().strip()

        self.assertNotEqual(state_id, "",
                            "Failed to get State ID from console output")
        self.assertTrue(len(state_id) > 0,
                        "Failed to get State ID from console output")
        self.assertRegex(state_id, r'^[0-9a-f-]{36}$')

        self.conn.commit()

        new_state_count = self.get_table_entries_count("states")
        self.assertEqual(new_state_count, initial_state_count +
                         1, "State was not added to DB")

        # 2. Create a City using the new state_id
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd(
                f'create City name="Reno" state_id="{state_id}"')
            city_id = output.getvalue().strip()

        self.assertNotEqual(city_id, "",
                            "Failed to get City ID from console output")
        self.assertTrue(len(city_id) > 0,
                        "Failed to get City ID from console output")
        self.assertRegex(city_id, r'^[0-9a-f-]{36}$')
        self.cities.append("City." + city_id)

    def test_12_create_city_non_existent_state_id(self):
        """
        Test that creating a City via the console with non_existent state_id
        does not add it to the database
        """
        with patch("sys.stdout", new=StringIO()) as output:
            args = 'create City name="Fremont" state_id="12345"'
            HBNBCommand().onecmd(args)
            city_id = output.getvalue().strip()

        self.assertEqual(city_id, "")
        self.assertFalse(city_id)

    def test_13_create_city_missing_state_id(self):
        """
        Test that creating a City via the console with missing state_id
        does not add it to the database
        """
        with patch("sys.stdout", new=StringIO()) as output:
            args = 'create City name="Fremont"'
            HBNBCommand().onecmd(args)
            city_id = output.getvalue().strip()

        self.assertEqual(city_id, "")
        self.assertFalse(city_id)


class Test_05_Place(TestDBStorageConsole):
    """Tests DBStorage integration with console commands for the Place model"""
    tablename = "places"

    model = TestDBStorageConsole.get_model_class(tablename)

    TestDBStorageConsole.create_attr_for_entries_created_based_table_name(
        tablename)

    def test_03_create_place_all_existing_attributes(self):
        """
        Test that creating a Place via the console adds it to the database.
        """

        self.assertNotEqual(self.get_table_entries_count(
            "users"), 0, "users table is empty")
        self.assertTrue(self.get_table_entries_count(
            "users") >= 1, "users table is empty")

        self.assertNotEqual(self.get_table_entries_count(
            "cities"), 0, "cities table is empty")
        self.assertTrue(self.get_table_entries_count(
            "cities") >= 1, "cities table is empty")

        # 1. Get a valid city_id from an existing city (required for Place)
        query = 'SELECT id from cities WHERE name=%s;'
        self.cursor.execute(query, ("San Francisco",))
        city_id = self.cursor.fetchone()[0]

        # 2. Get a valid user_id from an existing user (required for Place)
        query = 'SELECT id from users WHERE last_name=%s;'
        self.cursor.execute(query, ("Snow",))
        user_id = self.cursor.fetchone()[0]

        # 3. Create a Place using the user_id and city_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Place city_id="{city_id}" user_id="{user_id}"' +\
                ' name="Happy_place" description="No_description_provided"' +\
                ' number_rooms=3 number_bathrooms=1 ' +\
                'max_guest=6 price_by_night=120 latitude=37.773972 ' +\
                'longitude=-122.431297'
            HBNBCommand().onecmd(arg)
            place_id = output.getvalue().strip()

        self.assertNotEqual(place_id, "",
                            "Failed to get Place ID from console output")
        self.assertTrue(len(place_id) > 0,
                        "Failed to get Place ID from console output")
        self.assertRegex(place_id, r'^[0-9a-f-]{36}$')
        self.places.append("Place." + place_id)

    def test_06_create_place_missing_nullable_and_default_attributes(self):
        """
        Test that creating a Place via the console with
        missing_nullable_and_default_attributes adds it to the database.
        """
        initial_state_count = self.get_table_entries_count("states")
        initial_user_count = self.get_table_entries_count("users")
        initial_city_count = self.get_table_entries_count("cities")

        # 1. Create a User (required for Place)
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd(
                'create User email="johnsmith@example.com" ' +
                'password="password" first_name="John" last_name="Smith"')
            user_id = output.getvalue().strip()

        self.assertTrue(len(user_id) > 0,
                        "Failed to get State ID from console output")
        self.assertRegex(user_id, r'^[0-9a-f-]{36}$')

        # 2. Create a City (required for Place)

        # Create a new State first since City requires a valid state_id
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="Georgia"')
            state_id = output.getvalue().strip()

        self.assertTrue(len(state_id) > 0,
                        "Failed to get State ID from console output")
        self.assertRegex(state_id, r'^[0-9a-f-]{36}$')

        # create a new city using the state_id
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd(
                f'create City name="Atlanta" state_id="{state_id}"')
            city_id = output.getvalue().strip()

        self.assertTrue(len(city_id) > 0,
                        "Failed to get City ID from console output")
        self.assertRegex(city_id, r'^[0-9a-f-]{36}$')

        self.conn.commit()

        new_state_count = self.get_table_entries_count("states")
        new_user_count = self.get_table_entries_count("users")
        new_city_count = self.get_table_entries_count("cities")

        self.assertEqual(new_state_count, initial_state_count +
                         1, "State was not added to DB")
        self.assertEqual(new_user_count, initial_user_count +
                         1, "User was not added to DB")
        self.assertEqual(new_city_count, initial_city_count +
                         1, "City was not added to DB")

        # 3. Create a Place using the user_id and city_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Place city_id="{city_id}" ' +\
                f'user_id="{user_id}" name="Lovely_place"'
            HBNBCommand().onecmd(arg)
            place_id = output.getvalue().strip()

        self.assertNotEqual(place_id, "",
                            "Failed to get Place ID from console output")
        self.assertTrue(len(place_id) > 0,
                        "Failed to get Place ID from console output")
        self.assertRegex(place_id, r'^[0-9a-f-]{36}$')
        self.places.append("Place." + place_id)

    def test_12_create_place_missing_user_id(self):
        """
        Test that creating a Place via the console with missing user_id
        doesn't add it to the database.
        """
        self.assertNotEqual(self.get_table_entries_count(
            "cities"), 0, "cities table is empty")
        self.assertTrue(self.get_table_entries_count(
            "cities") >= 1, "cities table is empty")

        # 1. Get an existing city_id
        query = 'SELECT id from cities WHERE name=%s;'
        self.cursor.execute(query, ("San Francisco",))
        city_id = self.cursor.fetchone()[0]

        # 2. Create a Place without a user_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Place city_id="{city_id}" name="Wonderful_place"'
            HBNBCommand().onecmd(arg)
            place_id = output.getvalue().strip()

        self.assertEqual(place_id, "")
        self.assertFalse(place_id)

    def test_13_create_place_non_existent_user_id(self):
        """
        Test that creating a Place via the console with non_existent user_id
        doesn't add it to the database.
        """
        self.assertNotEqual(self.get_table_entries_count(
            "cities"), 0, "cities table is empty")
        self.assertTrue(self.get_table_entries_count(
            "cities") >= 1, "cities table is empty")

        # 1. Get an existing city_id
        query = 'SELECT id from cities WHERE name=%s;'
        self.cursor.execute(query, ("San Francisco",))
        city_id = self.cursor.fetchone()[0]

        # 2. Create a Place with a non-existent user_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Place city_id="{city_id}" user_id="12345" ' +\
                  'name="Wonderful_place"'
            HBNBCommand().onecmd(arg)
            place_id = output.getvalue().strip()

        self.assertEqual(place_id, "")
        self.assertFalse(place_id)

    def test_14_create_place_missing_city_id(self):
        """
        Test that creating a Place via the console with missing city_id
        doesn't add it to the database.
        """
        self.assertNotEqual(self.get_table_entries_count(
            "users"), 0, "users table is empty")
        self.assertTrue(self.get_table_entries_count(
            "users") >= 1, "users table is empty")

        # 2. Get an existing user_id
        query = 'SELECT id from users WHERE last_name=%s;'
        self.cursor.execute(query, ("Snow",))
        user_id = self.cursor.fetchone()[0]

        # 3. Create a Place without a city_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Place user_id="{user_id}" name="Joyful_place"'
            HBNBCommand().onecmd(arg)
            place_id = output.getvalue().strip()

        self.assertEqual(place_id, "")
        self.assertFalse(place_id)

    def test_15_create_place_non_existent_city_id(self):
        """
        Test that creating a Place via the console with non-existent city_id
        doesn't add it to the database.
        """
        self.assertNotEqual(self.get_table_entries_count(
            "users"), 0, "users table is empty")
        self.assertTrue(self.get_table_entries_count(
            "users") >= 1, "users table is empty")

        # 2. Get an existing user_id
        query = 'SELECT id from users WHERE last_name=%s;'
        self.cursor.execute(query, ("Snow",))
        user_id = self.cursor.fetchone()[0]

        # 3. Create a Place without a city_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Place city_id="12345" user_id="{user_id}" ' +\
                  'name="Joyful_place"'
            HBNBCommand().onecmd(arg)
            place_id = output.getvalue().strip()

        self.assertEqual(place_id, "")
        self.assertFalse(place_id)


class Test_06_Review(TestDBStorageConsole):
    """
    Tests DBStorage integration with console commands for the Review model.
    """
    tablename = "reviews"

    model = TestDBStorageConsole.get_model_class(tablename)

    TestDBStorageConsole.create_attr_for_entries_created_based_table_name(
        tablename)

    def test_03_create_review_all_existing_attributes(self):
        """
        Test that creating a Review via the console adds it to the database.
        """

        self.assertNotEqual(self.get_table_entries_count(
            "users"), 0, "users table is empty")
        self.assertTrue(self.get_table_entries_count(
            "users") >= 1, "users table is empty")

        self.assertNotEqual(self.get_table_entries_count(
            "places"), 0, "places table is empty")
        self.assertTrue(self.get_table_entries_count(
            "places") >= 1, "places table is empty")

        # 1. Get a valid place_id from an existing place (required for Review)
        query = 'SELECT id from places WHERE name=%s;'
        self.cursor.execute(query, ("Happy place",))
        place_id = self.cursor.fetchone()[0]
        print("city_id one place", place_id)

        # 2. Get a valid user_id from an existing user (required for Place)
        query = 'SELECT id from users WHERE last_name=%s;'
        self.cursor.execute(query, ("Snow",))
        user_id = self.cursor.fetchone()[0]
        print("user_id one place", user_id)

        # 3. Create a Review using the user_id and city_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Review place_id="{place_id}" user_id="{user_id}"' +\
                ' text="Amazing_place,_beautiful_beach"'
            HBNBCommand().onecmd(arg)
            review_id = output.getvalue().strip()

        self.assertNotEqual(review_id, "",
                            "Failed to get Review ID from console output")
        self.assertTrue(len(review_id) > 0,
                        "Failed to get Review ID from console output")
        self.assertRegex(review_id, r'^[0-9a-f-]{36}$')
        self.reviews.append("Review." + review_id)

    def test_06_create_review_all_valid_attributes(self):
        """
        Test that creating a Place via the console adds it to the database.
        """
        initial_state_count = self.get_table_entries_count("states")
        initial_user_count = self.get_table_entries_count("users")
        initial_city_count = self.get_table_entries_count("cities")
        initial_place_count = self.get_table_entries_count("places")

        # 1. Create a User (required for Place)
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd(
                'create User email="janesmith@example.com" ' +
                'password="password" first_name="Jane" last_name="Smith"')
            user_id = output.getvalue().strip()

        self.assertTrue(len(user_id) > 0,
                        "Failed to get State ID from console output")
        self.assertRegex(user_id, r'^[0-9a-f-]{36}$')

        # 2. Create a Place (required for Review)

        # Create a new State first since City requires a valid state_id
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="Louisiana"')
            state_id = output.getvalue().strip()

        self.assertTrue(len(state_id) > 0,
                        "Failed to get State ID from console output")
        self.assertRegex(state_id, r'^[0-9a-f-]{36}$')

        # create a new city using state_id since Place requires a valid city_id
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd(
                f'create City name="New_Orleans" state_id="{state_id}"')
            city_id = output.getvalue().strip()

        self.assertTrue(len(city_id) > 0,
                        "Failed to get City ID from console output")
        self.assertRegex(city_id, r'^[0-9a-f-]{36}$')

        # Create a Place using the user_id and city_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Place city_id="{city_id}" user_id="{user_id}" ' +\
                'name="Lovely_place"'
            HBNBCommand().onecmd(arg)
            place_id = output.getvalue().strip()

        self.conn.commit()

        new_state_count = self.get_table_entries_count("states")
        new_user_count = self.get_table_entries_count("users")
        new_city_count = self.get_table_entries_count("cities")
        new_place_count = self.get_table_entries_count("places")

        self.assertEqual(new_state_count, initial_state_count +
                         1, "State was not added to DB")
        self.assertEqual(new_user_count, initial_user_count +
                         1, "User was not added to DB")
        self.assertEqual(new_city_count, initial_city_count +
                         1, "City was not added to DB")
        self.assertEqual(new_place_count, initial_place_count +
                         1, "Place was not added to DB")

        # 3. Create a Review using the user_id and place_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Review place_id="{place_id}" ' +\
                f'user_id="{user_id}" text="Amazing_place,_beautiful_lounge"'
            HBNBCommand().onecmd(arg)
            review_id = output.getvalue().strip()

        self.reviews.append("Review." + review_id)
        self.assertTrue(len(review_id) > 0,
                        "Failed to get Review ID from console output")
        self.assertRegex(review_id, r'^[0-9a-f-]{36}$')

    def test_12_create_review_missing_user_id(self):
        """
        Test that creating a Review via the console with missing
        user_id doesn't add it to the database.
        """
        self.assertNotEqual(self.get_table_entries_count(
            "places"), 0, "places table is empty")
        self.assertTrue(self.get_table_entries_count(
            "places") >= 1, "places table is empty")

        # 1. Get a existing place_id
        query = 'SELECT id from places WHERE name=%s;'
        self.cursor.execute(query, ("Happy place",))
        place_id = self.cursor.fetchone()[0]

        # 3. Create a Review without a user_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Review place_id="{place_id}" ' +\
                  'text="Amazing_place,_beautiful_beach"'
            HBNBCommand().onecmd(arg)
            review_id = output.getvalue().strip()

        self.assertEqual(review_id, "")
        self.assertFalse(review_id)

    def test_13_create_review_non_existent_user_id(self):
        """
        Test that creating a Review via the console with non_existent user_id
        doesn't add it to the database.
        """
        self.assertNotEqual(self.get_table_entries_count(
            "places"), 0, "places table is empty")
        self.assertTrue(self.get_table_entries_count(
            "places") >= 1, "places table is empty")

        # 1. Get a existing place_id
        query = 'SELECT id from places WHERE name=%s;'
        self.cursor.execute(query, ("Happy place",))
        place_id = self.cursor.fetchone()[0]

        # 3. Create a Review with a non-existent user_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Review place_id="{place_id}" user_id="12345" ' +\
                  'text="Amazing_place,_beautiful_beach"'
            HBNBCommand().onecmd(arg)
            review_id = output.getvalue().strip()

        self.assertEqual(review_id, "")
        self.assertFalse(review_id)

    def test_14_create_review_missing_place_id(self):
        """
        Test that creating a Review via the console with missing
        place_id doesn't add it to the database
        """

        self.assertNotEqual(self.get_table_entries_count(
            "users"), 0, "users table is empty")
        self.assertTrue(self.get_table_entries_count(
            "users") >= 1, "users table is empty")

        # 1. Get an exisiting user_id
        query = 'SELECT id from users WHERE last_name=%s;'
        self.cursor.execute(query, ("Snow",))
        user_id = self.cursor.fetchone()[0]

        # 2. Create a Review without a place_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Review user_id="{user_id}" ' +\
                  'text="Amazing_place,_beautiful_beach"'
            HBNBCommand().onecmd(arg)
            review_id = output.getvalue().strip()

        self.assertEqual(review_id, "")
        self.assertFalse(review_id)

    def test_15_create_review_non_existent_place_id(self):
        """
        Test that creating a Review via the console with non_existent
        place_id doesn't add it to the database.
        """

        self.assertNotEqual(self.get_table_entries_count(
            "users"), 0, "users table is empty")
        self.assertTrue(self.get_table_entries_count(
            "users") >= 1, "users table is empty")

        # 1. Get an exisiting user_id
        query = 'SELECT id from users WHERE last_name=%s;'
        self.cursor.execute(query, ("Snow",))
        user_id = self.cursor.fetchone()[0]

        # 2. Create a Review with non-existent place_id
        with patch("sys.stdout", new=StringIO()) as output:
            arg = f'create Review place_id="12345" user_id="{user_id}" ' +\
                  'text="Amazing_place,_beautiful_beach"'
            HBNBCommand().onecmd(arg)
            review_id = output.getvalue().strip()

        self.assertEqual(review_id, "")
        self.assertFalse(review_id)


class Test_07_Amenity(TestDBStorageConsole):
    """
    Tests DBStorage integration with console commands for the Amenity model.
    """
    tablename = "amenities"

    model = TestDBStorageConsole.get_model_class(tablename)

    TestDBStorageConsole.create_attr_for_entries_created_based_table_name(
        tablename)

    def test_03_create_amenity_with_valid_attributes(self):
        """
        Test that creating an Amenity via the console adds it to the database
        """
        # Capture console output
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create Amenity name="Wifi"')
            amenity_id = output.getvalue().strip()

        self.amenities.append("Amenity." + amenity_id)
        self.assertTrue(len(amenity_id) > 0,
                        "Failed to get Amenity ID from console output")
        self.assertRegex(amenity_id, r'^[0-9a-f-]{36}$')

    def test_06_create_additional_amenity_with_valid_attributes(self):
        """
        Test that creating an Amenity via the console adds it to the database
        """
        # Capture console output
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create Amenity name="Oven"')
            amenity_id = output.getvalue().strip()

        self.amenities.append("Amenity." + amenity_id)
        self.assertTrue(len(amenity_id) > 0,
                        "Failed to get State ID from console output")
        self.assertRegex(amenity_id, r'^[0-9a-f-]{36}$')


if __name__ == "__main__":
    unittest.main()
