#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
User Module for HBNB project.

Defines the `User` class, which represents a user in the application.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """
    Represents a user in the HBNB project.

    Inherits from_:
        - BaseModel: Provides common attributes like `id`, `created_at`, and
                    `updated_at`.
        - Base: Enables SQLAlchemy ORM functionality.

    Attributes_:
        __tablename__ (str): The name of the MySQL table for users.
        email (Column or str): The user's email address (string, required).
        password (Column or str): The user's password (string, required).
        first_name (Column or str): The user's first name (string, optional).
        last_name (Column or str): The user's last name (string, optional).
        places (relationship or list): Relationship to `Place` objects if
                                        using DB storage.
        reviews (relationship or list): Relationship to `Review` objects if
                                        using DB storage.
    """

    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        places = relationship('Place',
                              backref='user',
                              cascade='all, delete, delete-orphan')

        reviews = relationship('Review',
                               backref='user',
                               cascade='all, delete, delete-orphan')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
