#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
DBStorage module for managing database storage in MySQL.

This module defines the `DBStorage` class, which provides methods
to interact with a MySQL database using SQLAlchemy.
"""
import os
import importlib
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place, place_amenity
from models.review import Review
from models.state import State
from models.user import User

__author__ = "Albert Mwanza"
__license__ = "MIT"
__date__ = "2025-02-12"
__version__ = "2.1"


class DBStorage:
    """
    This class manages storage of hbnb models in a MySQL database.

    Attributes_:
        __engine (sqlalchemy.engine.Engine): The database engine.
        __session (sqlalchemy.orm.scoped_session): The database session.
    """

    DB_CLASSES = [User, State, City, Amenity, Place, Review]

    __engine: None
    __session: None

    __objects = {}

    def __init__(self):
        """
        Initialize the DBStorage instance and set up the database connection.

        The connection URL is constructed using environment variables:
            - HBNB_MYSQL_USER: MySQL username
            - HBNB_MYSQL_PWD: MySQL password
            - HBNB_MYSQL_HOST: MySQL host
            - HBNB_MYSQL_DB: MySQL database name
            - HBNB_ENV: Application environment (e.g., 'test')

        If `HBNB_ENV` is set to 'test', all tables are dropped.
        """
        # Construct the database connection URL
        url_object = URL.create(
            "mysql+mysqldb",  # dialect+driver
            username=os.getenv("HBNB_MYSQL_USER"),
            password=os.getenv("HBNB_MYSQL_PWD"),
            host=os.getenv("HBNB_MYSQL_HOST"),
            database=os.getenv("HBNB_MYSQL_DB"),)

        # Create the database engine
        self.__engine = create_engine(url_object, pool_pre_ping=True)

        # Drop all tables if in test environment
        if os.getenv("HBNB_ENV") == "test":
            try:
                # Bind the engine to the Base's metadata
                Base.metadata.bind = self.__engine

                # Drop all tables defined in the Base
                Base.metadata.drop_all(self.__engine)

            except OperationalError as e:
                message = getattr(e, '_message')
                print(message().partition(" ")
                      [-1].strip('()').split(',')[-1])

    def all(self, cls=None):
        """Return a dictionary of models currently in storage."""
        if cls is not None:
            classes = ('BaseModel',
                       'User',
                       'Place',
                       'State',
                       'City',
                       'Amenity',
                       'Review')

            if isinstance(cls, str):
                if cls not in classes:
                    return {}

                try:
                    # Dynamically import the class
                    # Convert class name to module name
                    module_path = f"models.{cls.lower()}"
                    module = importlib.import_module(module_path)
                    # Get the class from the module
                    cls = getattr(module, cls)

                except (ImportError, AttributeError):
                    print("** class doesn't exist **")

            if cls in self.DB_CLASSES:
                for obj in self.__session.query(cls).all():
                    key = f"{type(obj).__name__}.{obj.id}"
                    self.__objects[key] = obj
            else:
                return {}
        else:
            for model in self.DB_CLASSES:
                for obj in self.__session.query(model).all():
                    key = f"{type(obj).__name__}.{obj.id}"
                    self.__objects[key] = obj

        return self.__objects

    def new(self, obj):
        """Add new object to storage dictionary."""
        self.__session.add(obj)

    def save(self):
        """Save storage dictionary to file."""
        self.__session.commit()

    def reload(self):
        """Load storage dictionary from file."""
        try:
            # Bind the engine to the Base's metadata
            Base.metadata.bind = self.__engine

            Base.metadata.create_all(self.__engine)

            session_factory = sessionmaker(bind=self.__engine,
                                           expire_on_commit=False)

            Session = scoped_session(session_factory)

        except OperationalError as e:
            message = getattr(e, '_message')
            print(message().partition(" ")
                  [-1].strip('()').split(',')[-1])
        else:
            self.__session = Session()

    def delete(self, obj=None):
        """Delete object from the storage."""
        if obj is not None:
            self.__session.delete(obj)

            try:
                del self.__objects[type(obj).__name__ + '.' + obj.id]

            except KeyError as e:
                pass

        self.save()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()

    def rollback(self):
        """Roll back the session to clear the invalid state."""
        self.__session.rollback()
