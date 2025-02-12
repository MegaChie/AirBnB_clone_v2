#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Place Module for HBNB project.

Defines the `Place` class, which represents accommodations available in the
system.

Handles relationships with `City`, `User`, `Review`, and `Amenity`.
"""
import os
from models.base_model import BaseModel, Base
# from models.amenity import Amenity
# from models.review import Review
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Column, String, ForeignKey, Float, Table
from typing import List


# association table for the many-to-many relationship
place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"),
           nullable=False, primary_key=True),
    Column("amenity_id", String(60), ForeignKey("amenities.id"),
           nullable=False, primary_key=True),
)


class Place(BaseModel, Base):
    """
    Represents a place (accommodation) in the HBNB project.

    Inherits from:
        - BaseModel: Provides common attributes like `id`, `created_at`, and
                    `updated_at`.
        - Base: Enables SQLAlchemy ORM functionality.

    Attributes_:
        __tablename__ (str): The name of the MySQL table for places.
        city_id (Column or str): The ID of the associated city (foreign key,
                                                                required).
        user_id (Column or str): The ID of the owner/user (foreign key,
                                                           required).
        name (Column or str): The name of the place (string, required).
        description (Column or str): A detailed description of the place.
        number_rooms (Column or int): The number of rooms in the place.
        number_bathrooms (Column or int): The number of bathrooms in the place.
        max_guest (Column or int): The maximum number of guests allowed.
        price_by_night (Column or int): The cost per night.
        latitude (Column or float): The latitude coordinate of the place.
        longitude (Column or float): The longitude coordinate of the place.
        reviews (relationship or property): A one-to-many relationship with
                                            `Review` (DB storage).
        amenities (relationship or property): A many-to-many relationship with
                                             `Amenity` (DB storage).
    """

    __tablename__ = "places"

    amenity_ids: List[str] = []

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=False, default=0.0)
    longitude = Column(Float, nullable=False, default=0.0)

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        reviews = relationship('Review',
                               backref='place',
                               cascade='all, delete, delete-orphan')

        amenities = relationship('Amenity',
                                 secondary='place_amenity',
                                 overlaps="place_amenities",
                                 viewonly=False)

    else:
        city_id: str = ""
        user_id: str = ""
        name: str = ""
        description: str = ""
        number_rooms: int = 0
        number_bathrooms: int = 0
        max_guest: int = 0
        price_by_night: int = 0
        latitude: float = 0.0
        longitude: float = 0.0

        @property
        def reviews(self):
            """Returns a list of `Review` instances related to this Place."""
            from models import storage
            from models.review import Review  # Avoid circular import issues

            return [review for review in storage.all(
                Review).values() if review.place_id == self.id]

        @property
        def amenities(self):
            """Returns a list of `Amenity` instances linked to this Place."""
            from models import storage
            from models.amenity import Amenity  # Avoid circular import issues

            return [amenity for amenity in storage.all(
                Amenity).values() if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Add an Amenity instance to this Place."""
            from models.amenity import Amenity  # Avoid circular import issues

            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
