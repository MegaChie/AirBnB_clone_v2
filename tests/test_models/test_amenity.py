#!/usr/bin/python3
""" """
import os
from models.amenity import Amenity
from tests.test_models.test_base_model import test_basemodel


class test_amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """Initialize the test class for Amenity."""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Tests the type of name attribute."""
        new = self.value()
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            self.assertNotEqual(type(new.name), str)
        else:
            self.assertEqual(type(new.name), type(None))
