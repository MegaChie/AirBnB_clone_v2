#!/usr/bin/python3
""" Module for testing  """
from tests.test_models.test_base_model import TestBasemodel
from models.place import Place


class TestPlace(TestBasemodel):
    """Represents the tests for the Place model."""
    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_amenity_ids(self):
        """Tests the type of amenity_ids."""
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)
