#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """State class"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", cascade="all, delete", backref="state")
    else:
        @property
        def cities(self):
            """Return any city with state_id equal to self.id"""
            from models import storage
            from models.city import City
            # list of all cities
            compCity = storage.all(City)
            # list of wanted sities
            wantCity = []
            for elem in compCity.values():
                if elem.state_id == self.id:
                    wantCity.append(elem)
            return wantCity
