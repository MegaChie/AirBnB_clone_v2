#!/usr/bin/python3
""" Module for testing  """
from tests.test_models.test_base_model import TestBasemodel
from models.state import State


class TestState(TestBasemodel):
    """Represents the tests for the State model."""
    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State
