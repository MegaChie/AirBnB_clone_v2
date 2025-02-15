#!/usr/bin/python3
"""State Module for HBNB project"""


import models
import sys

if 'storage' not in sys.modules:
    from models import storage
from models.city import city
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """State class representation for database"""
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City",  backref="state", cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    """Property method"""
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Get method for cities"""
            citiess = []
            for c in list(models.storage.all(City).values()):
                if c.state_id == self.id:
                    citiess.append(c)
            return citiess
