#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from models import storage_type, storage
import unittest
import os


@unittest.skipIf(storage_type == 'db', 'Tests not designed for DBStorage')
class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)


@unittest.skipUnless(storage_type == 'db', "Tests designed only for DBStorage")
class test_state_DB(unittest.TestCase):
    """State DB tests"""
    def setUp(self):
        """Setup a new State instance before each test"""
        self.state = State(name="Test_State")
        storage.new(self.state)
        storage.save()

    def tearDown(self):
        """Clean up the State instance after each test"""
        storage.delete(self.state)
        storage.save()

    def test_name(self):
        """tests that the name exists and matches"""
        self.assertEqual(type(self.state), State)
        self.assertEqual(type(self.state.name), str)
        self.assertEqual(self.state.name, "Test_State")

    def test_state_in_storage(self):
        """tests that the instance is in the database"""
        self.assertIn("State.{}".format(self.state.id), storage.all())
