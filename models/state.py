#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
import os
from sqlalchemy.orm import relationship
from models.city import City

storeType = os.environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """ State class """
    name = Column('name', String(128), nullable=False)
    __tablename__ = 'states'
    cities = relationship(
        'City',
        backref='state',
        cascade='all, delete, delete-orphan',
        passive_deletes=True
    )

    @property
    def cities(self):
        """cities filestorage getter function"""
        import models
        cityObjects = []
        results = models.storage.all('City').values()
        for c in results:
            if c.state_id == self.id:
                cityObjects.append(c)
        return cityObjects
