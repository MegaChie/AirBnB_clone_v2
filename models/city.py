#!/usr/bin/python3
"""city module for HBNB"""

from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Represents city class of MySQL database

    Inherits from SQLAlchemy Base and links to MySQL table cities

    Attribs:
        __tablename__ (str): Name of MySQL table to store Cities
        name (sqlalchemy String): Name of City
        state_id (sqlalchemy String): State id of City
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")