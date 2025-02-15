#!/usr/bin/python3
""" Module for testing """
from tests.test_models.test_base_model import TestBasemodel
from models.user import User


class TestUser(TestBasemodel):
    """Represents the tests for the User model."""
    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User
