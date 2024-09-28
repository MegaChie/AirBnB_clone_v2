#!/usr/bin/python3
"""Database storage for the HBNB project."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """Database storage engine for the HBNB project."""
    
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database storage engine."""
        username = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')

        db_url = f"mysql+mysqldb://{username}:{password}@{host}/{db_name}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of the given class or all classes."""
        objs_list = []
        if cls:
            if isinstance(cls, str):
                cls = globals().get(cls)
            if issubclass(cls, Base):
                objs_list = self.__session.query(cls).all()
            else:
                for subclass in Base.__subclasses__():
                    objs_list.extend(self.__session.query(subclass).all())
        else:
            objs_list = self.__session.query(State).all() + self.__session.query(City).all()  # Include other classes as needed

        obj_dict = {}
        for obj in objs_list:
            key = f"{obj.__class__.__name__}.{obj.id}"
            obj_dict[key] = obj
            del obj._sa_instance_state 
        return obj_dict
        
    def new(self, obj):
        """Add a new object to the current database session."""
        self.__session.add(obj)
    
    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()
    
    def delete(self, obj=None):
        """Delete an object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Remove the current session."""
        self.__session.remove()
