#!/usr/bin/env python3
"""State Module."""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class State(BaseModel, Base):
    """State class for states in the database."""

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship("City", back_populates="state", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initialize State instance."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """Return string representation of State."""
        return f"[State] ({self.id}) {self.name}"

    @property
    def cities(self):
        """Return the list of City instances associated with this State."""
        from models import storage
        return [city for city in storage.all(City).values() if city.state_id == self.id]

