#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Unit tests for Review"""
from tests.test_models.test_base_model import TestBaseModel
from models.review import Review


class TestReview(TestBaseModel):
    """Test cases for the Review class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def setUp(self):
        """Set up test environment"""
        self.review = self.value()  # Create a Review instance for testing

    def test_place_id(self):
        """Test that place_id exists and is a string"""
        self.assertTrue(hasattr(self.review, "place_id"))
        self.assertIsInstance(self.review.place_id, str)
        self.assertEqual(self.review.place_id, "")

    def test_user_id(self):
        """Test that user_id exists and is a string"""
        self.assertTrue(hasattr(self.review, "user_id"))
        self.assertIsInstance(self.review.user_id, str)
        self.assertEqual(self.review.user_id, "")

    def test_text(self):
        """Test that text exists and is a string"""
        self.assertTrue(hasattr(self.review, "text"))
        self.assertIsInstance(self.review.text, str)
        self.assertEqual(self.review.text, "")
