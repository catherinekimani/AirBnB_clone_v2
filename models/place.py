#!/usr/bin/python3
""" Place Module for HBNB project """
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models.review import Review


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False)
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
    p_reviews = relationship("Review", backref='place', cascade="all, delete")
    p_amenities = relationship(
                               "Amenity",
                               secondary=place_amenity,
                               viewonly=False
                               )

    @property
    def reviews(self):
        """Returns the reviews of this Place"""

        from models import storage
        reviews_of_place = []
        for value in storage.all(Review).values():
            if value.place_id == self.id:
                reviews_of_place.append(value)
        return reviews_of_place

    @property
    def amenities(self):
        """Returns the amenities of this Place"""

        from models import storage
        amenities_of_place = []
        for value in storage.all(Amenity).values():
            if value.id in self.amenity_ids:
                amenities_of_place.append(value)
        return amenities_of_place

    def amenities(self, value):
        """Adds an amenity to this Place"""
        if type(value) is Amenity:
            if value.id not in self.amenity_ids:
                self.amenity_ids.append(value.id)
