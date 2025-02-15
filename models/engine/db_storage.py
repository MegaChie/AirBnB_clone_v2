#!/usr/bin/python3
""" DBStorage module for HBNB project """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import os


class DBStorage:
    """ DBStorage class for HBNB project """
    # declare as None for use later
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize the DBStorage class """
        # set up the connection
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        # Create engine
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{db}',
            pool_pre_ping=True)
        # if test env, then drop tables
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query all objects in the database """
        # import classes
        from models.user import User
        from models.city import City
        from models.state import State
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
    
        objects = {}
        # classes to query
        classes = [User, State, City, Amenity, Place, Review]

        # if cls, query that class
        if cls:
            query = self.__session.query(cls).all()
            # assign key to object
            for obj in query:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        else:
            # query all classes
            for cls in classes:
                query = self.__session.query(cls).all()
                # assign key to object
                for obj in query:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """ Add a new object to the database """
        self.__session.add(obj)

    def save(self):
        """ Commit changes to the database """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete an object from the database """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Reload the database """
        # import classes
        from models.user import User
        from models.state import State
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review
        from models.city import City

        # create tables
        # Base.metadata.create_all(self.__engine)
        # create session, use scoped session for safety
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        # save session
        self.__session = Session()
