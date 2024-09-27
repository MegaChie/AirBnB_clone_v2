#!/usr/bin/env python3
"""DBStorage Module."""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
import models


class DBStorage:
    """DBStorage class to manage database storage."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage instance."""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects based on class name."""
        if cls:
            return {f"{cls.__name__}.{obj.id}": obj for obj in self.__session.query(cls).all()}
        return {f"{obj.__class__.__name__}.{obj.id}": obj for obj in self.__session.query(BaseModel).all()}

    def new(self, obj):
        """Add the object to the current session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize the current session."""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def get(self, cls, id):
        """Retrieve an object by class and id."""
        return self.__session.query(cls).get(id)

    def count(self, cls=None):
        """Count all objects in storage or of a specific class."""
        if cls:
            return self.__session.query(cls).count()
        return self.__session.query(BaseModel).count()

