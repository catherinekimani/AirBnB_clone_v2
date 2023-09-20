#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review


place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey("places.id")),
    Column('amenity_id', String(60), ForeignKey("amenities.id"))
)


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity",
                             secondary=place_amenity,
                             viewonly=False
                             )

    @property
    def reviews(self):
        """ Client Reviews """
        from models import storage
        m_list = []
        revs = storage.all('Review').values()
        for review in revs:
            if self.id == review.place_id:
                m_list.append(review)
        return m_list

    @property
    def amenities(self):
        """ add amenity to the place """
        from models import storage
        m_list = []
        amns = storage.all('Amenity').values()
        for amenity in amns:
            if self.id == amenity.amenity_ids:
                m_list.append(amenity)
        return m_list

    @amenities.setter
    def amenities(self, value):
        """Adds an amenity to this Place"""
        if type(value) is Amenity:
            if value.id not in self.amenity_ids:
                self.amenity_ids.append(value.id)
