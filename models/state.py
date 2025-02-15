#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
State Module for HBNB project.

Defines the `State` class, which represents a state in the application.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """
    Represents a state in the HBNB project.

    Inherits from_:
        - BaseModel: Provides common attributes like `id`, `created_at`, and
                        `updated_at`.
        - Base: Enables SQLAlchemy ORM functionality.

    Attributes_:
        __tablename__ (str): The name of the MySQL table for states.
        name (Column or str): The name of the state (string, required).
        cities (relationship or property): A relationship to `City` objects
                                          if using DB storage, otherwise a
                                          property returning related `City`
                                          instances.
    """

    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        cities = relationship('City',
                              backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name: str = ""

        @property
        def cities(self):
            """
            Returns a list of `City` instances related to this `State`
            when using file storage.

            Retrieves all `City` objects from storage and filters them
            based on `state_id`.
            """
            from models import storage
            from models.city import City

            return [city for city in storage.all(
                City).values() if city.state_id == self.id]
