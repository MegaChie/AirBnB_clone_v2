#!/usr/bin/python3
"""DBStorage module"""


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """DBStorage class"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(os.getenv('HBNB_MYSQL_USER'),
                    os.getenv('HBNB_MYSQL_PWD'),
                    os.getenv('HBNB_MYSQL_HOST'),
                    os.getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on all instances from the database"""
        insta = dict()
        classes = (User, State, City, Amenity, Place, Review)
        if cls is None:
            for c_t in classes:
                query = self.__session.query(c_t)
                for obj in query.all():
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    insta[key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                insta[key] = obj
        return insta

    def new(self, obj):
        """Adds object to the database"""
        self.__session.add(obj)

    def save(self):
        """Save all changes in the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables"""
        Base.metadata.create_all(self.__engine)
        sess_fac = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False)
        Session = scoped_session(sess_fac)
        self.__session = Session()

    def close(self):
         """call remove() method on the private session attribute"""
        self.__session.remove()
