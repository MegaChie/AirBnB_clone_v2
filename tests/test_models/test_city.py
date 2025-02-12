#!/usr/bin/python3
"""Unit tests for City"""
from tests.test_models.test_base_model import TestBaseModel
from models.city import City


class TestCity(TestBaseModel):
    """Test cases for the City class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """
        Test that state_id exists, is a string, and defaults to an empty string
        """
        new = self.value()
        self.assertTrue(hasattr(new, "state_id"))
        self.assertIsInstance(new.state_id, str)
        self.assertEqual(new.state_id, "")

    def test_name(self):
        """
        Test that name exists, is a string, and defaults to an empty string
        """
        new = self.value()
        self.assertTrue(hasattr(new, "name"))
        self.assertIsInstance(new.name, str)
        self.assertEqual(new.name, "")
