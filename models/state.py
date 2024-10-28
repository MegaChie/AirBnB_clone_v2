#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel):
    """ State class """
    # table represents states in the db
    __tablename__ = 'states'

    # create the relationship between state and cities
    # links the state and cities together back and forth
    # with thee backref, 
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        """ getter attribute cities that returns the list of City instances """
        # if storage is db then just return cities
        # else return all cities with state id
        if models.storage_t == 'db':
            return self.cities
        else:
            return [city for city in list(models.storage.all(City).values()) if city.state_id == self.id]
