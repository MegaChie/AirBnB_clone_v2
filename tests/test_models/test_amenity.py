#!/usr/bin/python3
"""Unit tests for Amenity"""
from tests.test_models.test_base_model import TestBaseModel
from models.amenity import Amenity


class test_Amenity(TestBaseModel):
    """Test cases for the Amenity class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Test that name is a string"""
        new = self.value()
        self.assertEqual(type(new.name), str)
        self.assertTrue(hasattr(new, "name"))
        self.assertEqual(new.name, "")
