#!/usr/bin/python3
""" Module for testing  """
from tests.test_models.test_base_model import TestBasemodel
from models.review import Review


class TestReview(TestBasemodel):
    """Represents the tests for the Review model."""
    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review
