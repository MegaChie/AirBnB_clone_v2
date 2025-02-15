#!/usr/bin/python3
"""Amenity class module"""

from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Represents Amenity for MySQL database

    Inherits from SQLAlchemy Base and links to  MySQL table amenities

    Attributes:
        __tablename__ (str): Name of MySQL table to store Amenities
        name (sqlalchemy String): Amenity name
        place_amenities (sqlalchemy relationship): Place-Amenity relationship
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   viewonly=False)