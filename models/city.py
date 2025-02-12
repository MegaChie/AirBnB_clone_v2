#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
City module for the HBNB project.

Defines the `City` class, which represents a city associated with a state.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """
    Represents a city in the HBNB project.

    Inherits from_:
        - BaseModel: Provides common attributes like `id`, `created_at`, and
                    `updated_at`.
        - Base: Enables SQLAlchemy ORM functionality.

    Attributes_:
        __tablename__ (str): The name of the MySQL table for cities.
        name (Column or str): The name of the city (string, required).
        state_id (Column or str): The ID of the associated state (foreign key,
                                                                  required).
        places (relationship): A one-to-many relationship with `Place`
                                (only for DB storage).
    """

    __tablename__ = "cities"

    name = Column(String(128), nullable=False)

    state_id = Column(String(60), ForeignKey("states.id"),
                      nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        places = relationship('Place',
                              backref='cities',
                              cascade='all, delete, delete-orphan')
    else:
        name: str = ""
        state_id: str = ""
