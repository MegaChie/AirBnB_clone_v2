#!/usr/bin/python3
""" City Module for HBNB project """
import os
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class City(BaseModel):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"

    state_id = (
        Column(String(60), ForeignKey("states.id"), nullable=False)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )
    name = (
        Column(String(128), nullable=False)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )
    places = (
        relationship(
            "Place", backref="cities", cascade="all, delete, delete-orphan"
        )
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else None
    )
