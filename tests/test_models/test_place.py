#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models import storage_type, storage
import unittest


@unittest.skipIf(storage_type == 'db', 'Tests not designed for DBStorage')
class test_Place(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.city_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_description(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.description), str)

    def test_number_rooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_rooms), int)

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), int)

    def test_max_guest(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.max_guest), int)

    def test_price_by_night(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.price_by_night), int)

    def test_latitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    def test_longitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    def test_amenity_ids(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)


@unittest.skipUnless(storage_type == 'db', "Tests designed only for DBStorage")
class test_place_DB(unittest.TestCase):
    """Place DB tests"""
    def setUp(self):
        """Setup a new Place instance before each test"""
        self.state = State(name="Test_State")
        storage.new(self.state)
        storage.save()
        self.city = City(name="Test_City", state_id=self.state.id)
        storage.new(self.city)
        storage.save()
        self.user = User(email="a@b.com", password="password")
        storage.new(self.user)
        storage.save()
        self.place = Place(user_id=self.user.id,
                           city_id=self.city.id,
                           name="Test_Place",
                           description="Test_Description",
                           number_rooms=3,
                           number_bathrooms=2,
                           max_guest=4,
                           price_by_night=100,
                           latitude=3.14,
                           longitude=-3.14)
        storage.new(self.place)
        storage.save()

    def test_city_id(self):
        """Test city_id is a string and valid foreign key."""
        self.assertEqual(type(self.place.city_id), str)
        self.assertEqual(self.place.city_id, self.city.id)

    def test_name(self):
        """Test name attribute."""
        self.assertEqual(type(self.place.name), str)
        self.assertEqual(self.place.name, "Test_Place")

    def test_description(self):
        """Test description attribute."""
        self.assertEqual(type(self.place.description), str)
        self.assertEqual(self.place.description, "Test_Description")

    def test_number_rooms(self):
        """Test number_rooms attribute."""
        self.assertEqual(type(self.place.number_rooms), int)
        self.assertEqual(self.place.number_rooms, 3)

    def test_number_bathrooms(self):
        """Test number_bathrooms attribute."""
        self.assertEqual(type(self.place.number_bathrooms), int)
        self.assertEqual(self.place.number_bathrooms, 2)

    def test_max_guest(self):
        """Test max_guest attribute."""
        self.assertEqual(type(self.place.max_guest), int)
        self.assertEqual(self.place.max_guest, 4)

    def test_price_by_night(self):
        """Test price_by_night attribute."""
        self.assertEqual(type(self.place.price_by_night), int)
        self.assertEqual(self.place.price_by_night, 100)

    def test_latitude(self):
        """Test latitude attribute."""
        self.assertEqual(type(self.place.latitude), float)
        self.assertEqual(self.place.latitude, 3.14)

    def test_longitude(self):
        """Test longitude attribute."""
        self.assertEqual(type(self.place.longitude), float)
        self.assertEqual(self.place.longitude, -3.14)
