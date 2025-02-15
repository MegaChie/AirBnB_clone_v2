#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage_type, storage
import unittest


@unittest.skipIf(storage_type == 'db', 'Tests not designed for DBStorage')
class test_review(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.text), str)


@unittest.skipUnless(storage_type == 'db', "Tests designed only for DBStorage")
class test_review_DB(unittest.TestCase):
    """Review DB tests"""
    def setUp(self):
        """Setup a new Review instance before each test"""
        self.state = State(name="Test_State")
        storage.new(self.state)
        storage.save()
        self.city = City(name="Test_City", state_id=self.state.id)
        storage.new(self.city)
        storage.save()
        self.user = User(email="a@b.com", password="password")
        storage.new(self.user)
        storage.save()
        self.place = Place(user_id=self.user.id,
                           city_id=self.city.id,
                           name="Test_Place",
                           description="Test_Description",
                           number_rooms=3,
                           number_bathrooms=2,
                           max_guest=4,
                           price_by_night=100,
                           latitude=3.14,
                           longitude=-3.14)
        storage.new(self.place)
        storage.save()
        self.review = Review(text="This is a test review.",
                             place_id=self.place.id,
                             user_id=self.user.id)
        storage.new(self.review)
        storage.save()

    def tearDown(self):
        """Clean up the class instances after each test"""
        storage.delete(self.review)
        storage.delete(self.place)
        storage.delete(self.user)
        storage.delete(self.city)
        storage.delete(self.state)
        storage.save()

    def test_review_instance_in_storage(self):
        """Test that the Review instance is stored in the database"""
        key = "Review." + self.review.id
        self.assertIn(key, storage.all())

    def test_review_text_in_storage(self):
        """Test that the Review instance in storage has the correct text"""
        key = "Review." + self.review.id
        self.assertEqual(storage.all()[key].text, "This is a test review.")

    def test_review_retrieval_by_id(self):
        """Test retrieval of the review from storage by its ID"""
        review_from_storage = storage.all().get("Review." + self.review.id)
        self.assertIsNotNone(review_from_storage)

    def test_review_retrieved_has_correct_id(self):
        """Test that the retrieved review's ID matches the original ID"""
        review_from_storage = storage.all().get("Review." + self.review.id)
        self.assertEqual(review_from_storage.id, self.review.id)

    def test_review_retrieved_has_correct_text(self):
        """Test that the retrieved review's text matches the expected value"""
        review_from_storage = storage.all().get("Review." + self.review.id)
        self.assertEqual(review_from_storage.text, "This is a test review.")

    def test_review_place_id_type(self):
        """Test that place_id is a string"""
        self.assertEqual(type(self.review.place_id), str)

    def test_review_place_id_matches_place(self):
        """Test that place_id matches the Place's ID"""
        self.assertEqual(self.review.place_id, self.place.id)

    def test_review_user_id_type(self):
        """Test that user_id is a string"""
        self.assertEqual(type(self.review.user_id), str)

    def test_review_user_id_matches_user(self):
        """Test that user_id matches the User's ID"""
        self.assertEqual(self.review.user_id, self.user.id)

    def test_review_text_type(self):
        """Test that text is a string"""
        self.assertEqual(type(self.review.text), str)

    def test_review_text_value(self):
        """Test that text matches the expected value"""
        self.assertEqual(self.review.text, "This is a test review.")
