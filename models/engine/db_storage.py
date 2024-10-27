#!/usr/bin/python3
""" DBStorage Module """
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
	""" DBStorage class """
	__engine = None
	__session = None

	def __init__(self):
		""" initialize DBStorage class """
		# retrieve env variables
		user = os.getenv('HBNB_MYSQL_USER')
		password = os.getenv('HBNB_MYSQL_PWD')
		host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
		database = os.getenv('HBNB_MYSQL_DB')

		# create engine, basically the bridge between python and database
		self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, password, host, database), pool_pre_ping=True)

		# drop all tables if env is equal to test
		if os.getenv('HBNB_ENV') == 'test':
			Base.metadata.drop_all(self.__engine)

		# -----------------------------------
		# Need to complete this part
	def all(self, cls=None):
			""" query on the current database """
		
	def new (self, obj):
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
