#!/usr/bin/python3
""" Module for testing  """
from models.city import City
from tests.test_models.test_base_model import TestBasemodel


class TestCity(TestBasemodel):
    """Represents the tests for the City model."""
    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City
