#!/usr/bin/python3
""" Module for testing Basemodel """
from datetime import datetime
import json
import os
import unittest
from models.base_model import BaseModel, Base


class TestBasemodel(unittest.TestCase):
    """Represents the tests for the BaseModel."""

    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Performs some operations before the tests are run."""
        pass

    def tearDown(self):
        """Performs some operations after the tests are run"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """Tests the initialization of the model class.
        """
        self.assertIsInstance(self.value(), BaseModel)
        if self.value is not BaseModel:
            self.assertIsInstance(self.value(), Base)
        else:
            self.assertNotIsInstance(self.value(), Base)

    def test_default(self):
        """Tests the type of value stored."""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Tests kwargs with an int."""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Tests kwargs with an int."""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_save(self):
        """Tests the save function of the BaseModel class."""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Tests the __str__ function of the BaseModel class."""
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_kwargs_none(self):
        """Tests kwargs that is empty."""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """Tests kwargs with one key-value pair."""
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertTrue(hasattr(new, 'Name'))

    def test_id(self):
        """Tests the type of id."""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Tests the type of created_at."""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """Tests the type of updated_at."""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_delete(self):
        """Tests the delete function of the BaseModel class."""
        from models import storage
        i = self.value()
        i.save()
        self.assertTrue(i in storage.all().values())
        i.delete()
        self.assertFalse(i in storage.all().values())
