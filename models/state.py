#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade="all, delete", backref="state")

    if storage_type != 'db':
        @property
        def cities(self):
            """
            get list of City instances with state_id
            equals to the current State.id
            """
            Cities = models.storage.all("City").values()
            List = []
            for city in Cities:
                if city.state_id == self.id:
                    List.append(city)
            return List
