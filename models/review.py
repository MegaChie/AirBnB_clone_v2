#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Review module for the HBNB project.

Defines the `Review` class, which stores user reviews related to places.
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """
    Represents a review given by a user for a specific place.

    Inherits from_:
        - BaseModel: Provides common attributes like `id`, `created_at`, and
                     `updated_at`.
        - Base: Enables SQLAlchemy ORM functionality.

    Attributes_:
        __tablename__ (str): The name of the MySQL table for reviews.
        place_id (Column or str): The ID of the associated place (foreign key,
                                                                  required).
        user_id (Column or str): The ID of the user who wrote the review
                                (foreign key, required).
        text (Column or str): The review content (string, required).
    """

    __tablename__ = "reviews"

    place_id = Column(String(60), ForeignKey('places.id'), nullable=False, )
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") != 'db':
        place_id: str = ""
        user_id: str = ""
        text: str = ""
