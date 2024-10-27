#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel):
    """ The city class, contains state ID and name """
    # create table for cities class
    __tablename__ = 'cities'
    # give data to attributes
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)  # state.id
    name = Column(String(128), nullable=False)
