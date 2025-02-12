#!/usr/bin/python3
""" """
import os
import unittest
import json
from datetime import datetime, timedelta
from unittest.mock import patch
from models.base_model import BaseModel


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Skipping: not using DBStorage")
class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        if os.path.exists("file.json"):
            os.remove('file.json')

    def tearDown(self):
        try:
            os.remove('file.json')
        except FileNotFoundError as e:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        i = self.value()

        try:
            delattr(i, '_sa_instance_state')
        except AttributeError:
            pass

        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}

        new = self.value(**n)
        self.assertIn('Name', dir(new))
        self.assertEqual(getattr(new, 'Name'), 'test')

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertIsInstance(new.updated_at, datetime)

    @patch('models.base_model.datetime')
    def test_updated_at(self, mock_datetime):
        """Test that updated_at is updated correctly"""
        # Configure the mock to return a specific datetime object
        mock_now = datetime.now()
        mock_datetime.now.return_value = mock_now

        # Create a new BaseModel instance
        new = self.value()

        # Check that updated_at is a datetime object
        self.assertIsInstance(new.updated_at, datetime)

        # Check that created_at and updated_at are initially the same
        self.assertEqual(new.created_at, new.updated_at)

        # Save the old updated_at value
        old_updated_at = new.updated_at

        # Simulate 5 seconds later
        mock_datetime.now.return_value = old_updated_at + timedelta(seconds=5)
        new.save()

        # Convert the instance to a dictionary and back to a BaseModel instance
        n = new.to_dict()

        # Temporarily un-mock datetime to allow datetime.strptime
        # to work correctly
        with patch('models.base_model.datetime',
                   wraps=datetime) as mock_datetime_unmocked:
            new = BaseModel(**n)

        # Check that created_at and updated_at are no longer the same
        self.assertNotEqual(new.created_at, new.updated_at)

        # Check that updated_at is greater than the old updated_at
        self.assertTrue(new.updated_at > old_updated_at)
