#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
from models import storage_type, storage
import unittest


@unittest.skipIf(storage_type == 'db', 'Tests not designed for DBStorage')
class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)


@unittest.skipUnless(storage_type == 'db', "Tests designed only for DBStorage")
class test_amenity_DB(unittest.TestCase):
    """Amenity DB tests"""
    def setUp(self):
        """Setup a new User instance before each test"""
        self.amenity = Amenity(name="Chair")
        storage.new(self.amenity)
        storage.save()

    def tearDown(self):
        """Teardown of all User instances after each test"""
        storage.delete(self.amenity)
        storage.save()

    def test_amenity_instance_in_storage(self):
        """Test that the Amenity instance is stored in the database"""
        key = "Amenity." + self.amenity.id
        self.assertIn(key, storage.all())

    def test_amenity_name_in_storage(self):
        """Test that the Amenity instance in storage has the correct name"""
        key = "Amenity." + self.amenity.id
        self.assertEqual(storage.all()[key].name, "Chair")

    def test_amenity_retrieval_by_id(self):
        """Test retrieval of the Amenity from storage by its ID"""
        amenity_from_storage = storage.all().get("Amenity." + self.amenity.id)
        self.assertIsNotNone(amenity_from_storage)

    def test_amenity_name_type(self):
        """Test that the name attribute is a string"""
        self.assertEqual(type(self.amenity.name), str)

    def test_amenity_name_value(self):
        """Test that the name matches the expected value"""
        self.assertEqual(self.amenity.name, "Chair")
