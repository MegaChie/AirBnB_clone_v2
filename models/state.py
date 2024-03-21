#!/usr/bin/python3
""" State Module for HBNB project """
import models
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """State class"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")
    if getenv("HBNB_TYPE_STORAGE") != "db":
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
