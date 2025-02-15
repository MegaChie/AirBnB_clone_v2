#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table, Integer, Float
from sqlalchemy.orm import relationship
from models.engine import storage_type

# Define the association table for the many-to-many relationship
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """This class defines a place by various attributes"""
    __tablename__ = 'places'

    if storage_type == 'db':
        # Define columns
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        # Define the relationship with Amenity through the association table
        amenities = relationship("Amenity", secondary=place_amenity,
                                 backref="places", viewonly=False)
        # Defines relationships with User
        user = relationship("User", back_populates="places")
        # Defines relationships with City
        cities = relationship("City", back_populates="places")
        # Defines relationships with Review
        reviews = relationship("Review", back_populates="place",
                               cascade="all, delete-orphan")
    else:
        user_id = ""
        city_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        # amenities = []
        amenity_ids = []

        # @property
        # def amenity_ids(self):
        #     """Return a list of Amenity ids linked to the Place"""
        #     return [amenity.id for amenity in self.amenities]

        @property
        def amenities(self):
            """Return a list of Amenity instances linked to the Place"""
            from models import storage
            from models.amenity import Amenity
            list_amenities = []
            for amen in storage.all(Amenity).values():
                if amen.id in self.amenity_ids():
                    list_amenities.append(amen)
            return list_amenities

        @amenities.setter
        def amenities(self, amenity):
            """Add Amenity.id to the list of amenity_ids"""
            from models.amenity import Amenity
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)

        # @amenity_ids.setter
        # def amenity_ids(self, amenity):
        #     """Add Amenity.id to the list of amenity_ids"""
        #     from models.amenity import Amenity
        #     if isinstance(amenity, str):  # Expecting an Amenity ID
        #         from models import storage
        #         amenity_obj = storage.get(Amenity, amenity)
        #         if amenity_obj:
        #             self.amenities.append(amenity_obj)

        def remove_amenity(self, amenity):
            """Remove Amenity from the Place"""
            from models.amenity import Amenity
            if isinstance(amenity, Amenity):
                self.amenities.remove(amenity)
            elif isinstance(amenity, str):  # If passed an Amenity ID
                amenity_obj = next((a for a in self.amenities
                                    if a.id == amenity), None)
                if amenity_obj:
                    self.amenities.remove(amenity_obj)

        @property
        def reviews(self):
            """Return a list of Reviews instances linked to the Place"""
            from models import storage
            from models.review import Review
            list_reviews = []
            for rev in storage.all(Review).values():
                if rev.place_id == self.id:
                    list_reviews.append(rev)
            return list_reviews
