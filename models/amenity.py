#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.engine import storage_type


class Amenity(BaseModel, Base):
    """This class defines an amenity with a name and its
    relationship to places."""

    __tablename__ = 'amenities'

    if storage_type == 'db':
        # Define the name column with a maximum length of 128 characters
        name = Column(String(128), nullable=False)

        # Define the many-to-many relationship with Place
        # places = relationship("Place", secondary="place_amenity",
        #                       viewonly=False)
    else:
        name = ""

        def __init__(self, *args, **kwargs):
            """Initializes an instance of Amenity"""
            super().__init__(*args, **kwargs)
