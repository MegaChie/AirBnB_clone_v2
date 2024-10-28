#!/usr/bin/python3
""" DBStorage Module """
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
    """ DBStorage class """
    # declaring engine and session to be used later
    # engine is connector to database
    __engine = None
    # session helps keep track of changes
    # and work with data tables as objecjs
    __session = None

    def __init__(self):
        """ initialize DBStorage class """
        # retrieve env variables
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        database = os.getenv('HBNB_MYSQL_DB')

        # create engine, basically the bridge between python and database
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{database}', pool_pre_ping=True)

        # drop all tables if env is equal to test
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database """
        # import all class models
        from models.user import User
        from models.city import City
        from models.state import State
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        
		# list of all classes
        classes = [User, State, City, Amenity, Place, Review]
        # empty dict
        objects = {}
        
		# if cls, then its just that specific class
        # requesting information and if successful retrieving it
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        # if no cls, then its all classes
        else:
            for cls in classes:
                query = self.__session.query(cls).all()
                for obj in query:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects

	# these all modify the database session
    def new(self, obj):
        """ new object """
        self.__session.add(obj)

    def save(self):
        """ save object """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete object """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create all the tables in db"""
        # import all classes from base
        from models.user import User
        from models.state import State
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review
        from models.city import City

        # create all tables from db
        Base.metadata.create_all(self.__engine)
        # setup session maker
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # scoped session helps keep it cleaner and safer
        # while doing things within database
        self.__session = scoped_session(Session)
