#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Unit tests for Place"""
from tests.test_models.test_base_model import TestBaseModel
from models.place import Place


class TestPlace(TestBaseModel):
    """Test cases for the Place class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def setUp(self):
        """Set up test environment"""
        self.place = self.value()  # Create a Place instance for testing

    def test_city_id(self):
        """Test that city_id exists and is a string"""
        self.assertTrue(hasattr(self.place, "city_id"))
        self.assertIsInstance(self.place.city_id, str)
        self.assertEqual(self.place.city_id, "")  # Assuming default is empty

    def test_user_id(self):
        """Test that user_id exists and is a string"""
        self.assertTrue(hasattr(self.place, "user_id"))
        self.assertIsInstance(self.place.user_id, str)
        self.assertEqual(self.place.user_id, "")

    def test_name(self):
        """Test that name exists and is a string"""
        self.assertTrue(hasattr(self.place, "name"))
        self.assertIsInstance(self.place.name, str)
        self.assertEqual(self.place.name, "")

    def test_description(self):
        """Test that description exists and is a string"""
        self.assertTrue(hasattr(self.place, "description"))
        self.assertIsInstance(self.place.description, str)
        self.assertEqual(self.place.description, "")

    def test_number_rooms(self):
        """Test that number_rooms exists and is an integer"""
        self.assertTrue(hasattr(self.place, "number_rooms"))
        self.assertIsInstance(self.place.number_rooms, int)
        self.assertEqual(self.place.number_rooms, 0)

    def test_number_bathrooms(self):
        """Test that number_bathrooms exists and is an integer"""
        self.assertTrue(hasattr(self.place, "number_bathrooms"))
        self.assertIsInstance(self.place.number_bathrooms, int)
        self.assertEqual(self.place.number_bathrooms, 0)

    def test_max_guest(self):
        """Test that max_guest exists and is an integer"""
        self.assertTrue(hasattr(self.place, "max_guest"))
        self.assertIsInstance(self.place.max_guest, int)
        self.assertEqual(self.place.max_guest, 0)

    def test_price_by_night(self):
        """Test that price_by_night exists and is an integer"""
        self.assertTrue(hasattr(self.place, "price_by_night"))
        self.assertIsInstance(self.place.price_by_night, int)
        self.assertEqual(self.place.price_by_night, 0)

    def test_latitude(self):
        """Test that latitude exists and is a float"""
        self.assertTrue(hasattr(self.place, "latitude"))
        self.assertIsInstance(self.place.latitude, float)
        self.assertEqual(self.place.latitude, 0.0)

    def test_longitude(self):
        """Test that longitude exists and is a float"""
        self.assertTrue(hasattr(self.place, "longitude"))
        self.assertIsInstance(self.place.longitude, float)
        self.assertEqual(self.place.longitude, 0.0)  # Fixed the mistake

    def test_amenity_ids(self):
        """Test that amenity_ids exists and is a list"""
        self.assertTrue(hasattr(self.place, "amenity_ids"))
        self.assertIsInstance(self.place.amenity_ids, list)
        self.assertEqual(self.place.amenity_ids, [])
