#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker, Session
from os import getenv

classes = {"User": User, "State": State, "City": City, "Amenity": Amenity,
           "Place": Place, "Review": Review}


class DBStorage:
    """This class manages storage of hbnb models in MySql format"""
    __engine = None
    __session = None

    def __init__(self):
        """ initiate the class to a desired valueue"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}"
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session (self.__session)"""
        objDic = {}
        if cls:
            for row in self.__session.query(cls).all():
                objDic.update({"{}.{}".
                                format(type(cls).__name__, row.id,): row})
        else:
            for key, value in all_classes.items():
                for row in self.__session.query(value):
                    objDic.update({"{}.{}".
                                    format(type(row).__name__, row.id,): row})
        return objDic

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            theObj = classes[type(obj).__name__]
            self.__session.query(theObj).filter(theObj.id == obj.id).delete()

    def reload(self):
        """Create all tables in the database using feature of SQLAlchemy"""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sess)
    
    def close(self):
        """Close private session"""
        self.__session.close()
