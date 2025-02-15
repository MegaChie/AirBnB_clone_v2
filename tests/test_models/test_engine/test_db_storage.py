#!/usr/bin/python3
"""Unit tests for the DBStorage class."""
from models.engine.db_storage import DBStorage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models import storage_type, storage
import unittest


@unittest.skipIf(storage_type != 'db', "Tests designed only for DBStorage")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class."""

    def setUp(self):
        """Set up objects for testing."""
        self.state = State(name="Test_State")
        self.city = City(name="Test_City", state_id=self.state.id)
        self.user = User(email="user@example.com", password="password")
        self.place = Place(user_id=self.user.id,
                           city_id=self.city.id,
                           name="Test Place",
                           description="Test Description",
                           number_rooms=2,
                           number_bathrooms=1,
                           max_guest=4,
                           price_by_night=100)
        self.review = Review(text="This is a test review.",
                             place_id=self.place.id,
                             user_id=self.user.id)

        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.new(self.review)
        storage.save()  # Save to DB

    def tearDown(self):
        """Clean up the instances after each test."""
        storage.delete(self.review)
        storage.delete(self.place)
        storage.delete(self.user)
        storage.delete(self.city)
        storage.delete(self.state)
        storage.save()  # Ensure all objects are removed from DB

    def test_review_in_storage(self):
        """Test that the Review instance is stored in the database."""
        key = "Review.{}".format(self.review.id)
        self.assertIn(key, storage.all())

    def test_review_text_in_storage(self):
        """Test that the Review instance in storage has the correct text."""
        key = "Review.{}".format(self.review.id)
        self.assertEqual(storage.all()[key].text, self.review.text)

    def test_review_retrieval_by_id(self):
        """Test retrieval of the review from storage by its ID."""
        review_from_storage = storage.all().get(
            "Review.{}".format(self.review.id))
        self.assertIsNotNone(review_from_storage)

    def test_review_user_id(self):
        """Test that user_id is correctly assigned."""
        review_from_storage = storage.all().get(
            "Review.{}".format(self.review.id))
        self.assertEqual(review_from_storage.user_id, self.user.id)

    def test_review_place_id(self):
        """Test that place_id is correctly assigned."""
        review_from_storage = storage.all().get(
            "Review.{}".format(self.review.id))
        self.assertEqual(review_from_storage.place_id, self.place.id)

    def test_review_instance_type(self):
        """Test that the instance is of type Review."""
        self.assertIsInstance(self.review, Review)

    def test_all_storage(self):
        """Test that all instances are correctly stored."""
        all_objects = storage.all()
        self.assertIn("State.{}".format(self.state.id), all_objects)
        self.assertIn("City.{}".format(self.city.id), all_objects)
        self.assertIn("User.{}".format(self.user.id), all_objects)
        self.assertIn("Place.{}".format(self.place.id), all_objects)
        self.assertIn("Review.{}".format(self.review.id), all_objects)

    def test_delete_review(self):
        """Test deleting the review."""
        storage.delete(self.review)
        storage.save()  # Ensure deletion
        self.assertNotIn("Review.{}".format(self.review.id), storage.all())


# If you want to run the tests directly
if __name__ == '__main__':
    unittest.main()
