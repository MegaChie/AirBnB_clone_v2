from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    id = Column(String(60), primary_key=True, nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
    places = relationship("Place", backref="cities",
                          cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """ init city """
        super().__init__(*args, **kwargs)
