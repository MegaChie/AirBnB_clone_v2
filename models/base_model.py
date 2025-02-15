#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module defines common attributes and methods for all hbnb models."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """
    A base class for all hbnb models.

    This class defines common attributes and methods for all models
    that inherit from it. It is marked as an abstract class to prevent
    direct table creation.

    Attributes_:
        id (Column): A unique identifier for each instance.
        created_at (Column): Timestamp when the instance was created.
        updated_at (Column): Timestamp when the instance was last updated.
    """

    __abstract__ = True  # Prevents table creation for BaseModel

    # Mark this class as an abstract to prevent its table creation
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiate a new model."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ("created_at", "updated_at"):
                        setattr(self, key,
                                datetime.strptime(kwargs[f'{key}'],
                                                  '%Y-%m-%dT%H:%M:%S.%f'))
                    else:
                        setattr(self, key, value)

    def __str__(self):
        """Return a string representation of the instance."""
        __dict__copy = self.__dict__.copy()

        try:
            __dict__copy.pop('_sa_instance_state')

        except KeyError:
            pass

        return f"[{type(self).__name__}] ({self.id}) {__dict__copy}"

    def save(self):
        """Update updated_at with current time when instance is changed."""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format."""
        return_dict = {"__class__": type(self).__name__}

        for key, value in self.__dict__.copy().items():
            if key != '_sa_instance_state':  # updates
                if key in ("created_at", "updated_at"):
                    return_dict[key] = value.isoformat()
                else:
                    return_dict[key] = value

        return return_dict

    def delete(self):
        """Delete instance from the storage."""
        from models import storage

        storage.delete(self)  # updates
