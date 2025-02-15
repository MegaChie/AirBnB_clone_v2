#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage, storage_type
import os


@unittest.skipIf(storage_type == 'db', 'BaseModel not used in DBStorage')
class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        storage.new(new)  # Ensure the object is added to storage
        temp = storage.all()[f'BaseModel.{new.id}']  # Get object from storage
        self.assertTrue(temp is new)  # Check if it's the same instance

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        storage.new(new)
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        new.save()  # Save to file
        self.assertTrue(os.path.exists('file.json'))  # Ensure file exists

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.new(new)  # Ensure the object is added to storage
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.new(new)  # Add the object to storage
        storage.save()  # Save it to the file
        storage.reload()  # Reload from file
        loaded = storage.all().get(f'BaseModel.{new.id}')  # Get loaded object
        self.assertIsNotNone(loaded)  # Ensure loaded is not None
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])  # ID

    def test_reload_empty(self):
        """ Test loading from an empty file """
        with open(storage._FileStorage__file_path, 'w') as f:
            f.write('')  # Create an empty file

        with self.assertRaises(ValueError):  # Ensure ValueError is raised
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertIsNone(storage.reload())

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        storage.new(new)  # Add object to storage
        new.save()  # Save to file
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        storage.new(new)  # Ensure object is added to storage
        _id = new.to_dict()['id']
        temp = list(storage.all().keys())[0]  # Get the first key
        self.assertEqual(temp, 'BaseModel.{}'.format(_id))  # Check format

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)


if __name__ == '__main__':
    unittest.main()
