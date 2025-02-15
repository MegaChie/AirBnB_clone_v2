#!/usr/bin/python3
"""
This module define the DBStorage
"""

from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Class for DB Storage DBStorage class."""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage class."""
        username = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        db_name = getenv("HBNB_MYSQL_DB")
        db_host = getenv("HBNB_MYSQL_HOST")
        url = f"mysql+mysqldb://{username}:{password}@{db_host}/{db_name}"
        self.__engine = create_engine(url, pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of objects from the database.
        """
        models = [User, City, Place, Amenity, Review, State]
        result = {}
        if cls is None:
            for model in models:
                query = self.__session.query(model)
                for obj in query.all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    result[key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                result[key] = obj
        return result

    def save(self):
        """
        Commits changes to the database.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the database.
        """
        if obj is not None:
            self.__session.delete(obj)

    def new(self, obj):
        """
        Adds a new object to the session.
        """
        if obj is not None:
            self.__session.add(obj)

    def reload(self):
        """
        Creates all tables in the database.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
