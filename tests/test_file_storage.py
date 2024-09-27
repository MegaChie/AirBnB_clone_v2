#!/usr/bin/env python3
import unittest
from models.engine.file_storage import FileStorage
from models.state import State

class TestFileStorage(unittest.TestCase):
    """ Test the FileStorage class """

    def setUp(self):
        """ Set up the test case with a new FileStorage instance. """
        self.fs = FileStorage()
        self.state1 = State()
        self.state1.name = "California"
        self.fs.new(self.state1)
        self.fs.save()

        self.state2 = State()
        self.state2.name = "Nevada"
        self.fs.new(self.state2)
        self.fs.save()

    def test_all_with_one_state(self):
        """ Test all method with only one State """
        self.fs.delete(self.state2)
        all_states = self.fs.all(State)
        self.assertEqual(len(all_states), 1)

    def test_all_with_two_states(self):
        """ Test all method with two States """
        all_states = self.fs.all(State)
        self.assertEqual(len(all_states), 2)

    def test_all_with_two_states_and_one_city(self):
        """ Test all method with two States and one City """
        from models.city import City  # Assuming you have a City class
        city = City()
        city.name = "Las Vegas"
        self.fs.new(city)
        self.fs.save()
        
        all_states = self.fs.all(State)
        self.assertEqual(len(all_states), 2)
        all_cities = self.fs.all(City)
        self.assertEqual(len(all_cities), 1)

    def test_all_filtered_by_class(self):
        """ Test all method with cls argument """
        from models.city import City  # Assuming you have a City class
        city = City()
        city.name = "Las Vegas"
        self.fs.new(city)
        self.fs.save()
        
        all_states = self.fs.all(State)
        self.assertEqual(len(all_states), 2)
        all_cities = self.fs.all(City)
        self.assertEqual(len(all_cities), 1)

    def test_delete_with_none(self):
        """ Test delete method with obj as None """
        initial_count = len(self.fs.all())
        self.fs.delete(None)
        self.assertEqual(initial_count, len(self.fs.all()))

    def test_delete_with_object(self):
        """ Test delete method with an object """
        self.fs.delete(self.state1)
        all_states = self.fs.all(State)
        self.assertEqual(len(all_states), 1)

if __name__ == "__main__":
    unittest.main()
