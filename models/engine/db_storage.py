#!/usr/bin/python3
"""Defines the DBStorage engine."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
import os
# Add other model imports as needed


mysql_user = os.getenv('HBNB_MYSQL_USER')
mysql_password = os.getenv('HBNB_MYSQL_PWD')
mysql_host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
mysql_db = os.getenv('HBNB_MYSQL_DB')


class DBStorage:
    """Represents the database storage engine."""

    __engine = None
    __session = None

    classes = {
            'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
            }

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                mysql_user, mysql_password,
                mysql_host, mysql_db
            ),
            pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def all(self, cls=None):
        """Query all objects based on class or all classes."""
        result_dict = {}
        if cls and cls in DBStorage.classes.values():
            query = self.__session.query(cls).all()
            for item in query:
                result_dict['{}.{}'.format(cls.__name__, item.id)] = item
        else:
            query = []
            for model_class in DBStorage.classes.values():
                query.extend(self.__session.query(model_class).all())
            for item in query:
                result_dict['{}.{}'.format(
                    item.__class__.__name__, item.id)] = item
        self.__session.expire_all()
        return result_dict

    def new(self, obj):
        """Add a new object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database."""
        try:
            self.__session.commit()
            self.close()
        except Exception as e:
            print("Error during commit: {}".format(e))
            self.__session.rollback()

    def reload(self):
        """Reload data from the database."""
        Base.metadata.create_all(self.__engine)
        if self.__session:
            self.close()
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)
            self.save()

    def close(self):
        """Session Closer"""
        self.__session.remove()
