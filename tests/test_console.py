#!/usr/bin/python3
"""Defines unittests for console.py."""
import os
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.file_storage import FileStorage


class TestHBNBCommand(unittest.TestCase):
    """Unittests for testing the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """HBNBCommand testing setup.

        Temporarily rename any existing file.json.
        Reset FileStorage objects dictionary.
        Create an instance of the command interpreter.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """HBNBCommand testing teardown.

        Restore original file.json.
        Delete the test HBNBCommand instance.
        """
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.HBNB

    def setUp(self):
        """Reset FileStorage objects dictionary."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Delete any created file.json."""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_create_for_errors(self):
        """Test create command errors."""
        # Test if class name is missing
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create")
            self.assertIn("** class name missing **", f.getvalue())
        
        # Test if class doesn't exist
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create asdfsfsd")
            self.assertIn("** class doesn't exist **", f.getvalue())

    def test_create_command_validity(self):
        """Test create command."""
        # Create BaseModel instance and capture its ID
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            bm = f.getvalue().strip()

        # Extract only the ID from the output
        bm_id = bm.split('\n')[-1]

        # Test if the created instance is in the output of "all" command
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all BaseModel")
            self.assertIn(bm_id, f.getvalue())

def test_create_command_with_kwargs(self):
    """Test create command with kwargs."""
    # Test create command with additional key-value pairs
    with patch("sys.stdout", new=StringIO()) as f:
        call = ('create Place city_id="0001" name="My_house" number_rooms=4 latitude=37.77 longitude=43.434')
        self.HBNB.onecmd(call)
        pl = f.getvalue().strip()

    # Extract only the ID from the output
    pl_id = pl.split('\n')[-1]

    # Test if the created instance and kwargs are in the output of "all" command
    with patch("sys.stdout", new=StringIO()) as f:
        self.HBNB.onecmd("all Place")
        output = f.getvalue()
        self.assertIn(pl_id, output)
        self.assertIn("'city_id': '0001'", output)
        self.assertIn("'name': 'My house'", output)
        self.assertIn("'number_rooms': '4'", output)  # Still expecting string '4'
        self.assertIn("'latitude': '37.77'", output)  # Expecting string '37.77'
        self.assertIn("'longitude': '43.434'", output)  # Expecting string '43.434'

if __name__ == "__main__":
    unittest.main()
