#!/usr/bin/env python3
"""City class module for AirBnB clone."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """Represents a city for the AirBnB clone."""
    
    __tablename__ = 'cities'
    
    name = Column(String(128), nullable=False)
    
    places = relationship("Place", back_populates="city", cascade="all, delete-orphan")
