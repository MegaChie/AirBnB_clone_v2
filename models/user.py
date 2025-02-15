#!/usr/bin/python3
"""This module defines a class User"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.engine import storage_type


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    if storage_type == 'db':
        # Class attributes representing columns
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        # Relationship with Place
        places = relationship("Place", back_populates="user",
                              cascade="all, delete-orphan")
        # Relationship with Review
        reviews = relationship("Review", back_populates="user",
                               cascade="all, delete-orphan")

        # Optionally, add unique constraint to email if needed
        __table_args__ = (
            {'sqlite_autoincrement': True},  # For SQLite, if you're using it
        )

    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
