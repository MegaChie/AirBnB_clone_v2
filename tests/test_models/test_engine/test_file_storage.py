#!/usr/bin/python3
""" Module for testing file storage"""
import os
import unittest
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from models.engine.file_storage import FileStorage


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Skipping: not using DBStorage")
class BaseTestFileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    model = None
    __file = "file.json"

    def setUp(self):
        """ Set up test environment """
        if self.model is None:
            self.skipTest("Skipping BaseTestFileStorage since it has no model")

        if os.path.exists(self.__file):
            os.remove(self.__file)

        storage._FileStorage__objects.clear()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove(self.__file)
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = self.model()
        storage.new(new)  # added

        self.assertIn(new, storage.all().values())

    def test_all(self):
        """ __objects is properly returned """
        new = self.model()
        storage.new(new)  # added
        storage.save()  # added
        temp = storage.all()
        self.assertIsInstance(temp, dict)
        self.assertIn(new, storage.all().values())

    def test_model_instantiation(self):
        """ Json file is not created on a model instantiation """
        new = self.model()
        self.assertFalse(os.path.exists(self.__file))

    def test_empty(self):
        """ Data is saved to file """
        new = self.model()
        thing = new.to_dict()
        new.save()
        new2 = self.model(**thing)
        self.assertNotEqual(os.path.getsize(self.__file), 0)

    def test_save(self):
        """ FileStorage save method """
        new = self.model()
        storage.new(new)  # added
        storage.save()
        self.assertTrue(os.path.exists(self.__file))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = self.model()
        storage.new(new)  # added
        storage.save()
        storage.reload()

        self.assertEqual(new.to_dict()['id'],
                         list(storage.all().values())[0].id)

    def test_reload_empty(self):
        """ Load from an empty file """
        with open(self.__file, 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = self.model()
        new.save()
        self.assertTrue(os.path.exists(self.__file))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertTrue(type(storage.all()) is dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = self.model()
        storage.new(new)  # added
        _id = new.to_dict()['id']

        self.assertIn(f'{self.model.__name__}' + '.' + _id,
                      storage.all().keys())

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        self.assertIsInstance(storage, FileStorage)

    def test_delete(self):
        """ Object is successfully deleted from __objects """
        new = self.model()
        storage.new(new)
        storage.save()
        self.assertIn(new, storage.all().values())
        storage.delete(new)
        self.assertNotIn(new, storage.all().values())

    def test_delete_nonexistent(self):
        """ Deleting a nonexistent object should not raise an error """
        new = self.model()
        storage.new(new)
        storage.save()
        self.assertIn(new, storage.all().values())
        storage.delete(new)  # Should not raise an error
        self.assertNotIn(new, storage.all().values())

    def test_all_with_class(self):
        """ all() method with class argument returns only matching objects """
        new1 = self.model()
        new2 = self.model()
        storage.new(new1)
        storage.new(new2)
        storage.save()
        self.assertIn(new1, storage.all(self.model).values())
        self.assertIn(new2, storage.all(self.model).values())
        self.assertTrue(all(self.assertIn(obj,
                                          storage.all().values()))
                        for obj in (new1, new2))

    def test_get_number_of_records(self):
        """ Get the number of current records in storage """
        new1 = self.model()
        new2 = self.model()
        storage.new(new1)
        storage.new(new2)
        storage.save()
        self.assertEqual(len(storage.all()), 2)


class TestBaseModelStorage(BaseTestFileStorage):
    model = BaseModel


class TestCityStorage(BaseTestFileStorage):
    model = City


class TestAmenityStorage(BaseTestFileStorage):
    model = Amenity


class TestPlaceStorage(BaseTestFileStorage):
    model = Place


class TestReviewStorage(BaseTestFileStorage):
    model = Review


class TestUserStorage(BaseTestFileStorage):
    model = User


class TestStateStorage(BaseTestFileStorage):
    model = State
