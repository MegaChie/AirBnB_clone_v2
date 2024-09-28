#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String, ForeignKey, Float, Integer, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from models.review import Review
from models.amenity import Amenity

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)

        # Relationship for reviews
        reviews = relationship('Review', cascade='all, delete-orphan', backref='place')

        # Association table for amenities
        place_amenity = Table(
            'place_amenity',
            Base.metadata,
            Column('place_id', ForeignKey('places.id'), primary_key=True, nullable=False),
            Column('amenity_id', ForeignKey('amenities.id'), primary_key=True, nullable=False)
        )
        # Relationship for amenities
        amenities = relationship('Amenity', secondary=place_amenity, 
                                 viewonly=False, back_populates="place_amenities")

    else:
        # Attributes for the FileStorage mode
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Returns the list of Review instances with place_id equal to current Place.id"""
            from models import storage
            return [review for review in storage.all(Review).values() if review.place_id == self.id]

        @property
        def amenities(self):
            """Returns the list of Amenity instances associated with the current Place."""
            from models import storage
            return [amenity for amenity in storage.all(Amenity).values() if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Adds an Amenity instance to the current Place."""
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
