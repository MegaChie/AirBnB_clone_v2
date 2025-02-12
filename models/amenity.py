#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Amenity module for the hbnb project.

Defines the `Amenity` class, which represents amenities available for places.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """
    Represents an amenity in the hbnb project.

    Inherits from_:
        - BaseModel: Provides common attributes like `id`, `created_at`, and
          `updated_at`.
        - Base: Enables SQLAlchemy ORM functionality.

    Attributes_:
        __tablename__ (str): The name of the MySQL table.
        name (Column or str): The name of the amenity.
        place_amenities (relationship): A many-to-many relationship with
                                        `Place` (only for DB storage).
    """

    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        place_amenities = relationship('Place',
                                       secondary='place_amenity',
                                       overlaps="place_amenities")
    else:
        name: str = ""
