#!/usr/bin/python3
""" Module for testing Amenity """
from tests.test_models.test_base_model import TestBasemodel
from models.amenity import Amenity


class TestAmenity(TestBasemodel):
    """Represents the tests for the Amenity model."""
    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity
