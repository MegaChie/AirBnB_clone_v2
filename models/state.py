#!/usr/bin/python3
"""State Module for HBNB project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models.engine import storage_type
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', back_populates='state',
                              cascade="all, delete-orphan")

    else:
        name = ''

        # getter
        def get_cities(self):
            from models.__init__ import storage
            from models.city import City
            list_cities = []
            cities_dict = storage.all(City)
            for city in cities_dict.values():
                if city.state_id == self.id:
                    list_cities.append(city)
            return list_cities
