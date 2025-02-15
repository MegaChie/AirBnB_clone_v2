#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""


import uuid
import models
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel"""
        DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key not in ['created_at', 'updated_at', 'id'] and key != "__class__":
                    raise KeyError(f"Invalid key: {key}")
                if key in ['created_at', 'updated_at']:
                    value = datetime.datetime.strptime(value, DATE_FORMAT)
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dictionary format"""
        res_dict = dict(self.__dict__)
        res_dict["__class__"] = str(type(self).__name__)
        res_dict["created_at"] = self.created_at.isoformat()
        res_dict["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in res_dict.keys():
            del res_dict['_sa_instance_state']
        return res_dict

    def delete(self):
        """Delete the current instance"""
        models.storage.delete(self)
