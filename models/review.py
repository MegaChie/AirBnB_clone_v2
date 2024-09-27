#!/usr/bin/env python3
"""Review class module for AirBnB clone."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Review(BaseModel, Base):
    """Represents a review for the AirBnB clone."""
    
    __tablename__ = 'reviews'
    
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="reviews", cascade="all, delete-orphan")
    place = relationship("Place", back_populates="reviews", cascade="all, delete-orphan")
