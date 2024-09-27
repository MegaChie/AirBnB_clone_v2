#!/usr/bin/env python3
""" Module for Place class """
from models.amenity import Amenity
from models.base_model import Base, BaseModel
from models.place_amenity import place_amenity
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

class Place(BaseModel, Base):
    """ Place class for storage in database """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False, back_populates="place_amenities")

    @property
    def amenities(self):
        """ Getter for amenities attribute """
        return [Amenity.get(id) for id in self.amenity_ids]

    @amenities.setter
    def amenities(self, amenity):
        """ Setter for amenities attribute """
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)
