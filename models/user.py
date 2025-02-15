#!/usr/bin/python3

""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from sqlalchemy import Column, String
from models.base_model import BaseModel, Base

"""
This module defines a class User that inherits from BaseModel and Base
"""


storage_type = getenv('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """Representation of a user """
    if storage_type == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
