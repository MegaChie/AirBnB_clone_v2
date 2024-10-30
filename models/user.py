#!/usr/bin/python3
"""This module defines a class User"""
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    # create table users
    __tablename__ = 'users'
    # create columns, string 128 char, not nullable
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    id = Column(String(60), primary_key=True, nullable=False)

    places = relationship("Place", backref="user",
                          cascade="all, delete, delete-orphan")
    reviews = relationship('Review', backref='user', cascade='all, delete')
