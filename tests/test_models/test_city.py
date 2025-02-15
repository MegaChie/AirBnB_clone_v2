#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
from models.state import State
from models import storage_type, storage
import unittest


@unittest.skipIf(storage_type == 'db', 'Tests not designed for DBStorage')
class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        # state_id still Column objects until specifically instantiated?
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        new = self.value()
        # name still Column objects until specifically instantiated?
        self.assertEqual(type(new.name), str)


@unittest.skipUnless(storage_type == 'db', "Tests designed only for DBStorage")
class test_city_DB(unittest.TestCase):
    """City DB tests"""
    def setUp(self):
        """Setup a new City instance before each test"""
        self.state = State(name="Test_State")
        storage.new(self.state)
        storage.save()
        self.city = City(name="Test_City", state_id=self.state.id)
        storage.new(self.city)
        storage.save()

    def tearDown(self):
        """Clean up the class instances after each test"""
        storage.delete(self.city)
        storage.delete(self.state)
        storage.save()

    def test_city_instance_in_storage(self):
        """Test that the City instance is stored in the database"""
        key = "City." + self.city.id
        self.assertIn(key, storage.all())

    def test_city_name_in_storage(self):
        """Test that the City instance in storage has the correct name"""
        key = "City." + self.city.id
        self.assertEqual(storage.all()[key].name, "Test_City")

    def test_city_retrieval_by_id(self):
        """Test retrieval of the city from storage by its ID"""
        city = storage.all().get("City." + self.city.id)
        self.assertIsNotNone(city)

    def test_city_retrieved_has_correct_id(self):
        """Test that the retrieved city's ID matches the original ID"""
        city = storage.all().get("City." + self.city.id)
        self.assertEqual(city.id, self.city.id)

    def test_city_retrieved_has_correct_name(self):
        """Test that the retrieved city's name matches the expected value"""
        city_from_storage = storage.all().get("City." + self.city.id)
        self.assertEqual(city_from_storage.name, "Test_City")

    def test_state_id_type(self):
        """Test that state_id is a string"""
        self.assertEqual(type(self.city.state_id), str)

    def test_state_id_matches_state(self):
        """Test that state_id matches the State's ID"""
        self.assertEqual(self.city.state_id, self.state.id)

    def test_city_name_type(self):
        """Test that name is a string"""
        self.assertEqual(type(self.city.name), str)

    def test_city_name_value(self):
        """Test that name matches the expected value"""
        self.assertEqual(self.city.name, "Test_City")
