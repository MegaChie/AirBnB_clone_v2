#!/usr/bin/python3
"""New engine database storage"""

from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """ Represent class DBStorage"""
    __engine = None
    __session = None
    class_dict = {
            'Amenity': Amenity,
            'City': City,
            'Place': Place,
            'State': State,
            'Review': Review,
            'User': User}

    def __init__(self):
        """ """
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return a dectionary"""
        dic = {}
        if type(cls) == str:
            cls = class_dict.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                dic[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in class_dict.values():
                for obj in self.__session.query(cls):
                    dic[obj.__class__.__name__ + '.' + obj.id] = obj
        return dic

    def new(self, obj):
        """add object to current d_b"""
        self.__session.add(obj)

    def save(self):
        """commit all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete an obj"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload obj"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()
