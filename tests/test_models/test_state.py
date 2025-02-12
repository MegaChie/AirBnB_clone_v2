#!/usr/bin/python3
"""Unit tests for the State class"""
from tests.test_models.test_base_model import TestBaseModel
from models.state import State


class test_state(TestBaseModel):
    """Test cases for the State class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """Test that name exists and is a string"""
        new = self.value()
        self.assertTrue(hasattr(new, "name"))
        self.assertIsInstance(new.name, str)
        self.assertEqual(new.name, "")  # Default value check
