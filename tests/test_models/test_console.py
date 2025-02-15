import unittest
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place

class TestHBNBCommand(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        storage.reset()  # Assuming there's a method to reset storage to clear previous data

    def tearDown(self):
        """Tear down test environment"""
        storage.reset()  # Clean up after each test

    def test_create_with_string_param(self):
        """Test object creation with a string parameter"""
        command = HBNBCommand()
        command.onecmd('create State name="California"')
        
        state_objs = storage.all(State)
        self.assertEqual(len(state_objs), 1)
        
        state = list(state_objs.values())[0]
        self.assertEqual(state.name, "California")

    def test_create_with_multiple_params(self):
        """Test object creation with multiple parameters"""
        command = HBNBCommand()
        command.onecmd('create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297')
        
        place_objs = storage.all(Place)
        self.assertEqual(len(place_objs), 1)
        
        place = list(place_objs.values())[0]
        self.assertEqual(place.city_id, "0001")
        self.assertEqual(place.user_id, "0001")
        self.assertEqual(place.name, "My little house")
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        self.assertEqual(place.latitude, 37.773972)
        self.assertEqual(place.longitude, -122.431297)

    def test_create_with_invalid_param(self):
        """Test object creation with an invalid parameter (should be skipped)"""
        command = HBNBCommand()
        command.onecmd('create State name="California" invalid_param="should_be_skipped"')
        
        state_objs = storage.all(State)
        self.assertEqual(len(state_objs), 1)
        
        state = list(state_objs.values())[0]
        self.assertFalse(hasattr(state, 'invalid_param'))

    def test_create_without_class_name(self):
        """Test object creation without specifying a class name"""
        command = HBNBCommand()
        with self.assertRaises(SystemExit):  # Command should exit with an error message
            command.onecmd('create')

    def test_create_with_nonexistent_class(self):
        """Test object creation with a non-existent class"""
        command = HBNBCommand()
        with self.assertRaises(SystemExit):  # Command should exit with an error message
            command.onecmd('create NonExistentClass')

if __name__ == "__main__":
    unittest.main()
