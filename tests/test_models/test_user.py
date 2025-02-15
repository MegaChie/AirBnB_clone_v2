#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from models.city import City
from models.user import User
from models import storage_type, storage
import unittest


@unittest.skipIf(storage_type == 'db', 'Tests not designed for DBStorage')
class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.password), str)


@unittest.skipUnless(storage_type == 'db', "Tests designed only for DBStorage")
class test_user_DB(unittest.TestCase):
    """User DB tests"""
    def setUp(self):
        """Setup a new User instance before each test"""
        self.user = User(email="a@b.com", password="password",
                         first_name="John", last_name="Roe")
        storage.new(self.user)
        storage.save()

    def tearDown(self):
        """Clean up the User instance after each test"""
        storage.delete(self.user)
        storage.save()

    def test_first_name_type(self):
        """Test that first_name is a string"""
        self.assertEqual(type(self.user.first_name), str)

    def test_last_name_type(self):
        """Test that last_name is a string"""
        self.assertEqual(type(self.user.last_name), str)

    def test_email_type(self):
        """Test that email is a string"""
        self.assertEqual(type(self.user.email), str)

    def test_password_type(self):
        """Test that password is a string"""
        self.assertEqual(type(self.user.password), str)

    def test_first_name_value(self):
        """Test that first_name can be set"""
        self.assertEqual(self.user.first_name, "John")

    def test_last_name_value(self):
        """Test that last_name can be set"""
        self.assertEqual(self.user.last_name, "Roe")

    def test_email_value(self):
        """Test that email can be set"""
        self.assertEqual(self.user.email, "a@b.com")

    def test_password_value(self):
        """Test that password can be set"""
        self.assertEqual(self.user.password, "password")

    def test_user_instance_in_storage(self):
        """Test that the User instance is stored in the database"""
        storage.new(self.user)
        storage.save()
        key = "User." + self.user.id
        self.assertIn(key, storage.all())

    def test_user_retrieval_by_id(self):
        """Test retrieval of the user from storage by its ID"""
        storage.new(self.user)
        storage.save()
        user_from_storage = storage.all().get("User." + self.user.id)
        self.assertIsNotNone(user_from_storage)

    def test_user_retrieved_has_correct_id(self):
        """Test that the retrieved user's ID matches the original ID"""
        storage.new(self.user)
        storage.save()
        user_from_storage = storage.all().get("User." + self.user.id)
        self.assertEqual(user_from_storage.id, self.user.id)

    def test_user_retrieved_has_correct_first_name(self):
        """Test that the retrieved user's
        first_name matches the expected value"""
        user = storage.all().get("User." + self.user.id)
        self.assertEqual(user.first_name, "John")

    def test_user_retrieved_has_correct_last_name(self):
        """Test that the retrieved user's
        last_name matches the expected value"""
        user = storage.all().get("User." + self.user.id)
        self.assertEqual(user.last_name, "Roe")

    def test_user_retrieved_has_correct_email(self):
        """Test that the retrieved user's email matches the expected value"""
        user = storage.all().get("User." + self.user.id)
        self.assertEqual(user.email, "a@b.com")

    def test_user_retrieved_has_correct_password(self):
        """Test that the retrieved user's
        password matches the expected value"""
        user = storage.all().get("User." + self.user.id)
        self.assertEqual(user.password, "password")
