#!/usr/bin/python3
""" Module for testing database storage"""

import os
import sys
import unittest
import MySQLdb
import sqlalchemy
from unittest.mock import patch, MagicMock
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from models.engine.db_storage import DBStorage
from sqlalchemy.orm import make_transient

__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-02-12"
__version__ = "2.1"

@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "Skipping: not using DBStorage")
class BaseTestDBStorage(unittest.TestCase):
    """Test cases for the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up database connection"""
        cls.storage = storage
        cls.storage.reload()  # Ensure the database session is reloaded
        cls.storage._DBStorage__objects.clear()

        try:
            # Setup MySQL connection using real credentials
            cls.conn = MySQLdb.connect(
                host=os.getenv("HBNB_MYSQL_HOST"),
                user=os.getenv("HBNB_MYSQL_USER"),
                password=os.getenv("HBNB_MYSQL_PWD"),
                database=os.getenv("HBNB_MYSQL_DB"),
                charset='utf8',
                port=3306)

        except MySQLdb.OperationalError as e:
            print(str(e).strip('()').split(',')[-1].strip())
            sys.exit(1)

        else:
            cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        """Close database connection"""
        cls.cursor.close()
        cls.conn.close()
        cls.storage.close()

    def setUp(self):
        """Set up test environment"""
        if not hasattr(self, 'tablename') or\
            self.tablename is None or\
                self.model is None:
            self.skipTest("Skipping test since it has no table name")

        # Clear the in-memory cache of objects
        self.storage._DBStorage__objects.clear()

    def tearDown(self):
        """Clean up after each test"""
        self.conn.commit()

    def test_01_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertTrue(type(self.storage.all()) is dict)

    def test_03_storage_var_created(self):
        """ DBStorage object storage created """
        self.assertIsInstance(self.storage, DBStorage)

    def get_table_entries_count(self, table=None):
        """Helper function to count records in a table"""
        allowed_tables = ('users',
                          'places',
                          'states',
                          'cities',
                          'amenities',
                          'reviews')

        if table is not None and table in allowed_tables:
            query = f"SELECT COUNT(*) FROM {table}"
        else:
            query = f"SELECT COUNT(*) FROM {self.tablename}"

        self.cursor.execute(query)
        return self.cursor.fetchone()[0]


class Test_01_TablesAreEmptyTestEnvironment(BaseTestDBStorage):
    """Confirm the tables are empty i.e storage instance __objects is empty
    when a storage instance is created and the test environment is 'test'."""

    def setUp(self):
        """Set up test environment"""
        if os.getenv("HBNB_ENV") != "test":
            self.skipTest(
                "Skipping test since development environ is not test")

        self.storage._DBStorage__objects.clear()

    @patch.dict(os.environ, {"HBNB_ENV": "test"})
    # Mock DBStorage.__init__
    @patch('models.engine.db_storage.DBStorage.__init__', return_value=None)
    def test_02_empty(self, mock_db_storage_init):
        """Confirm __objects is empty when HBNB_ENV is 'test'."""
        # Create a mock DBStorage instance
        mock_storage = DBStorage()

        # Ensure __objects is empty
        self.assertEqual(len(mock_storage._DBStorage__objects), 0)

        # Verify that __init__ was called (optional)
        mock_db_storage_init.assert_called_once()


class BaseTableTests(BaseTestDBStorage):
    model = None

    new_record = None

    def create_a_new_record_instance(self, **kwargs):
        if kwargs:
            self.new_record = self.model(**kwargs)
        else:
            self.new_record = self.model()

    def get_object_record_from_db_by_id(self, obj=None, table=None):
        """Helper function to count records in a table"""
        tables = ('users',
                  'places',
                  'states',
                  'cities',
                  'amenities',
                  'reviews')

        if table is not None and table in tables:
            query = f"SELECT * FROM {table} where id=%s"
        else:
            query = f"SELECT * FROM {self.tablename} where id=%s"

        if obj is not None:
            self.cursor.execute(query, (obj.id,))

        return self.cursor.fetchone()

    def assert_object_in_db(self, obj):
        """
        Helper method to assert that a record instance object exists in the
        database.
        """
        self.conn.commit()

        # Query the database directly to check if the object exists
        result = self.get_object_record_from_db_by_id(obj)

        self.assertIsNotNone(result, f"Object {obj} not found in the database")
        self.assertTrue(self.get_table_entries_count() >= 1)
        return result

    def assert_object_not_in_db(self, obj):
        """
        Helper method to assert that a record instance object exists in the
        database.
        """

        self.conn.commit()

        # Query the database directly to check if the object exists
        result = self.get_object_record_from_db_by_id(obj)

        self.assertIsNone(
            result,
            f"{self.new_record} object was not deleted from the database")
        self.assertNotIn(obj, self.storage.all().values())

    def update_record(self, **kwargs):
        """Update a new_record instance with provided kwargs"""
        for attr, value in kwargs.items():
            setattr(self.new_record, attr, value)

    def test_02_record_creation_without_kwargs(self):
        """Test creating and saving a new_record object without kwargs to
the database"""
        self.create_a_new_record_instance()

        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            self.new_record.save()

        # Roll back the session to clear the invalid state
        self.storage.rollback()

    def test_04_table_creation_valid_kwargs(self):
        """Test creating and saving a new_record object to the database"""
        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

    def test_05_new_record_attributes_property(self):
        # Verify the object is in the database

        new_record_attr = [attr
                           for attr, val in self.new_record.__dict__.items()
                           if not attr.startswith("_")
                           and attr not in ("created_at", "updated_at")
                           and val != []
                           and not isinstance(val, (User,
                                                    Place,
                                                    City,
                                                    Review,
                                                    Amenity,
                                                    State))
                           ]

        result = self.assert_object_in_db(self.new_record)

        if self.model == Amenity:
            try:
                del new_record_attr[new_record_attr.index("state_id")]
            except ValueError as e:
                pass

        for attr in new_record_attr:
            self.assertIn(getattr(self.new_record, attr), result)

    def test_06_record_deletion_from_db(self):
        """Test deleting a new_record object from the database"""
        initial_count = self.get_table_entries_count()

        self.assertTrue(self.get_table_entries_count() >= 1)

        # Delete new_record object and verify it is removed from the database
        self.storage.delete(self.new_record)

        self.conn.commit()

        self.assert_object_not_in_db(self.new_record)

        new_count = self.get_table_entries_count()
        self.assertTrue(new_count < initial_count)

        # Make the object transient
        make_transient(self.new_record)


class Test_08_User(BaseTableTests):
    """Test cases for the User model"""
    tablename = "users"

    model = User

    new_record = User(
        email="test@example1.com",
        password="password",
        first_name="Richard",
        last_name="Quest",
    )

    def test_07_user_update(self):
        """Test updating a User object in the database"""
#
        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

        self.assertEqual(self.new_record.email, "test@example1.com")
        self.assertEqual(self.new_record.first_name, "Richard")

        self.test_05_new_record_attributes_property()

        # Update the user's email and name
        self.update_record(first_name="Jane", email="test@example2.com")

        self.assertEqual(self.new_record.email, "test@example2.com")
        self.assertEqual(self.new_record.first_name, "Jane")

        self.storage.save()

        # Verify the changes in the database
        self.assert_object_in_db(self.new_record)

        self.test_05_new_record_attributes_property()

        query = F"SELECT * from {self.tablename} WHERE first_name=%s"

        self.cursor.execute(query, ("Jane",))

        result = self.cursor.fetchone()

        self.assertIsNotNone(result, "User not updated")

    def test_08_user_creation_missing_kwargs(self):
        new_user1 = self.model(email="johndoe@example.com",
                               first_name="John",
                               last_name="Doe")

        new_user2 = self.model(password="password",
                               first_name="John",
                               last_name="Doe")

        new_user3 = self.model(email="bond@doubleoseven.com",
                               password="password",
                               last_name="bond")

        new_user4 = self.model(email="test@example.com",
                               password="password",
                               first_name="John")

        for user in (new_user1, new_user2, new_user3, new_user4):
            with self.assertRaises(sqlalchemy.exc.IntegrityError):
                user.save()
                # Roll back the session to clear the invalid state
            self.storage.rollback()


class Test_09_State(BaseTableTests):
    """Test cases for the State model"""
    tablename = "states"

    model = State

    new_record = State(name="Texas")

    def test_07_state_update(self):
        """Test updating a User object in the database"""
        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

        self.assertEqual(self.new_record.name, "Texas")

        self.test_05_new_record_attributes_property()

        # Update the state's name
        self.update_record(name="Illinois")

        self.assertEqual(self.new_record.name, "Illinois")

        self.storage.save()

        # Verify the changes in the database
        self.assert_object_in_db(self.new_record)

        self.test_05_new_record_attributes_property()

        query = F"SELECT * from {self.tablename} WHERE name=%s"

        self.cursor.execute(query, ("Illinois",))

        result = self.cursor.fetchone()

        self.assertIsNotNone(result, "State not updated")


class Test_10_City(BaseTableTests):
    """Test cases for the City model"""
    tablename = "cities"

    model = City

    new_state = State(name="Massachusetts")

    new_record = City(name="Boston", state_id=new_state.id)
    updated_record = None

    def test_04_table_creation_valid_kwargs(self):
        """Test creating and saving a new_record object to the database"""
        self.storage.new(self.new_state)
        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

    def test_07_city_update(self):
        """Test updating a User object in the database"""
        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

        self.assertEqual(self.new_record.name, "Boston")

        self.test_05_new_record_attributes_property()

        # Update the city's name
        self.update_record(name="Amherst")
        self.assertEqual(self.new_record.name, "Amherst")

        self.storage.save()

        # Verify the changes in the database
        self.assert_object_in_db(self.new_record)

        self.test_05_new_record_attributes_property()

        query = F"SELECT * from {self.tablename} WHERE name=%s"

        self.cursor.execute(query, ("Amherst",))

        result = self.cursor.fetchone()

        self.assertIsNotNone(result, "City not updated")

        setattr(self, 'updated_record', self.new_record)

    def test_08_city_state_relationship(self):
        """Test the relationship between City and State"""
        state_id = self.new_state.id

        # Verify the relationship in the database
        query = """SELECT cities.name, cities.id
FROM cities
JOIN states ON cities.state_id=states.id
WHERE states.id=%s;"""
        self.cursor.execute(query, (state_id,))

        result = self.cursor.fetchone()

        city_name, city_id = result

        self.assertEqual(self.new_record.name, city_name)
        self.assertEqual(self.new_record.id, city_id)


class Test_11_Place(BaseTableTests):
    """Test cases for the Place model"""
    tablename = "places"

    model = Place

    new_user = User(
        email="therock@wwe.ent",
        password="therock",
        first_name="Dwane",
        last_name="Johnson",
    )

    new_state = State(name="Hawaii")

    new_city = City(name="Holualoa", state_id=new_state.id)

    new_record = Place(name="Grand Vacation Club",
                       city_id=new_city.id,
                       user_id=new_user.id,
                       description="Hilton Grand Vacations Club Kings" +
                       "Land Waikoloa")

    def test_04_table_creation_valid_kwargs(self):
        """Test creating and saving a new_record object to the database"""
        self.storage.new(self.new_user)
        self.storage.new(self.new_state)
        self.storage.new(self.new_city)
        self.storage.save()

        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

    def test_07_place_update(self):
        """Test updating a User object in the database"""
        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

        self.assertEqual(self.new_record.name, "Grand Vacation Club")

        self.test_05_new_record_attributes_property()

        # Update the state's name
        self.update_record(name="Sheraton",
                           description="Sheraton Waikiki Beach Resort")

        self.assertEqual(self.new_record.name, "Sheraton")
        self.assertEqual(self.new_record.description,
                         "Sheraton Waikiki Beach Resort")

        self.storage.save()

        # Verify the changes in the database
        self.assert_object_in_db(self.new_record)

        self.test_05_new_record_attributes_property()

        query = F"SELECT * from {self.tablename} WHERE name=%s"

        self.cursor.execute(query, ("Sheraton",))

        result = self.cursor.fetchone()

        self.assertIsNotNone(result, "Place not updated")

    def test_08_place_city_user_relationship(self):
        """Test the relationship between City, User and State"""
        city_id = self.new_city.id
        user_id = self.new_user.id

        # Verify the relationship in the database
        query = """SELECT places.name, places.id
FROM places
JOIN cities ON places.city_id=cities.id
JOIN users ON places.user_id=users.id
WHERE cities.id=%s
AND users.id=%s;"""
        self.cursor.execute(query, (city_id, user_id,))

        result = self.cursor.fetchone()

        place_name, place_id = result

        self.assertEqual(self.new_record.name, place_name)
        self.assertEqual(self.new_record.id, place_id)


class Test_12_Review(BaseTableTests):
    """Test cases for the Review model"""
    tablename = "reviews"

    model = Review

    new_user = User(
        email="fred@futuristic.net",
        password="theflintstones",
        first_name="Fred",
        last_name="Flintstone",
    )

    new_state = State(name="Florida")

    new_city = City(name="Orlando", state_id=new_state.id)

    new_place = Place(name="Futuristic Resorts",
                      city_id=new_city.id,
                      user_id=new_user.id,
                      description="Description not provided")

    new_record = Review(place_id=new_place.id,
                        user_id=new_user.id,
                        text="This is a great place!")

    def test_04_table_creation_valid_kwargs(self):
        """Test creating and saving a new_record object to the database"""
        self.storage.new(self.new_user)
        self.storage.new(self.new_state)
        self.storage.new(self.new_city)
        self.storage.new(self.new_place)
        self.storage.save()

        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

    def test_07_review_update(self):
        """Test updating a User object in the database"""
        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

        self.assertEqual(self.new_record.text, "This is a great place!")

        self.test_05_new_record_attributes_property()

        # Update the state's name
        self.update_record(text="This place is amazing!")

        self.assertEqual(self.new_record.text, "This place is amazing!")

        self.storage.save()

        # Verify the changes in the database
        self.assert_object_in_db(self.new_record)

        self.test_05_new_record_attributes_property()

        query = F"SELECT * from {self.tablename} WHERE text=%s"

        self.cursor.execute(query, ("This place is amazing!",))

        result = self.cursor.fetchone()

        self.assertIsNotNone(result, "Review not updated")

    def test_08_review_place_user_relationship(self):
        """Test the relationship between City, User and State"""
        place_id = self.new_place.id
        user_id = self.new_user.id

        # Verify the relationship in the database
        query = """SELECT reviews.text, reviews.id
FROM reviews
JOIN places ON reviews.place_id=places.id
JOIN users ON reviews.user_id=users.id
WHERE places.id=%s
AND users.id=%s;"""
        self.cursor.execute(query, (place_id, user_id,))

        result = self.cursor.fetchone()

        review, review_id = result

        self.assertEqual(self.new_record.text, review)
        self.assertEqual(self.new_record.id, review_id)


class Test_13_Amenity(BaseTableTests):
    """Test cases for the Amenity model"""
    tablename = "amenities"

    model = Amenity

    new_user = User(
        email="jj@spageage.com",
        password="theflintstones",
        first_name="Judy",
        last_name="Jetson",
    )

    new_state = State(name="Michigan")

    new_city = City(name="Detroit", state_id=new_state.id)

    new_place = Place(name="Space Age World",
                      city_id=new_city.id,
                      user_id=new_user.id,
                      description="A futuristic place")

    new_review = Review(place_id=new_place.id,
                        user_id=new_user.id,
                        text="This is a fantastic place!")

    new_record = Amenity(name="Wifi")

    def test_04_table_creation_valid_kwargs(self):
        """Test creating and saving a new_record object to the database"""
        self.storage.new(self.new_user)
        self.storage.new(self.new_state)
        self.storage.new(self.new_city)
        self.storage.new(self.new_place)
        self.storage.new(self.new_review)
        self.storage.save()

        self.new_record.state_id = self.new_state.id

        self.storage.new(self.new_record)
        self.storage.save()
        self.new_record.save()

        self.assert_object_in_db(self.new_record)

    def test_07_amenity_update(self):
        """Test updating a User object in the database"""
        self.storage.new(self.new_record)
        self.storage.save()

        self.assert_object_in_db(self.new_record)

        self.assertEqual(self.new_record.name, "Wifi")

        self.test_05_new_record_attributes_property()

        # Update the state's name
        self.update_record(name="Cable")

        self.assertEqual(self.new_record.name, "Cable")

        self.storage.save()

        # Verify the changes in the database
        self.assert_object_in_db(self.new_record)

        self.test_05_new_record_attributes_property()

        query = F"SELECT * from {self.tablename} WHERE name=%s"

        self.cursor.execute(query, ("Cable",))

        result = self.cursor.fetchone()

        self.assertIsNotNone(result, "Amenity not updated")

    def test_08_place_amenities_relationship(self):
        """Test the relationship between City, User and State"""
        place_id = self.new_place.id
        self.new_place.amenities.append(self.new_record)

        self.storage.save()

        # Verify the relationship in the database
        query = """SELECT amenities.name, amenities.id
FROM amenities
JOIN place_amenity ON place_amenity.amenity_id=amenities.id
JOIN places ON place_amenity.place_id=places.id
WHERE places.id=%s;"""
        self.cursor.execute(query, (place_id,))

        result = self.cursor.fetchone()

        amenity, amenity_id = result

        self.assertEqual(self.new_record.name, amenity)
        self.assertEqual(self.new_record.id, amenity_id)


if __name__ == '__main__':
    unittest.main()
