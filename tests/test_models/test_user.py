#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Unit tests for the User class"""
from tests.test_models.test_base_model import TestBaseModel
from models.user import User


class test_User(TestBaseModel):
    """Test cases for the User class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def setUp(self):
        """Set up test environment"""
        self.user = self.value()  # Create a User instance for testing

    def test_first_name(self):
        """Test that first_name exists and is a string"""
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertIsInstance(self.user.first_name, str)
        self.assertEqual(self.user.first_name, "")  # Default value check

    def test_last_name(self):
        """Test that last_name exists and is a string"""
        self.assertTrue(hasattr(self.user, "last_name"))
        self.assertIsInstance(self.user.last_name, str)
        self.assertEqual(self.user.last_name, "")  # Default value check

    def test_email(self):
        """Test that email exists and is a string"""
        self.assertTrue(hasattr(self.user, "email"))
        self.assertIsInstance(self.user.email, str)
        self.assertEqual(self.user.email, "")  # Default value check

    def test_password(self):
        """Test that password exists and is a string"""
        self.assertTrue(hasattr(self.user, "password"))
        self.assertIsInstance(self.user.password, str)
        self.assertEqual(self.user.password, "")  # Default value check
