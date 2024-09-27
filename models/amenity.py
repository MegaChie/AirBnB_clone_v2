#!/usr/bin/env python3
""" Module for Amenity class """
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ Amenity class for storage in database """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    place_amenities = relationship("Place", secondary="place_amenity", back_populates="amenities")

