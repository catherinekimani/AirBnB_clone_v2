#!/usr/bin/python3
"""This module defines a class to manage database storage"""
import os
from sqlalchemy import (create_engine)
import urllib.parse
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from models.place import Place, place_amenity
from models.user import User
from models.city import City
from models.state import State


class DBStorage:
    """class to manages storage of hbnb models in SQL db"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes SQL database storage"""
        user = os.getenv('HBNB_MYSQL_USER')
        pword = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        DATABASE_URL = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            user, pwrd, host, db_name
        )
        self.__engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dict of models in storage"""
        objects = dict()
        all_cls = (User, State, City, Amenity, Place, Review)
        if cls is None:
            for class_type in all_cls:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_keys = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_keys] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_keys = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_keys] = obj
        return objects

    def new(self, obj):
        """Adds new object to storage"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as exc:
                self.__session.rollback()
                raise exc

    def save(self):
        """Commits the session changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Removes an object from the db"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete(
                synchronize_session=False
            )

    def reload(self):
        """Loads storage db"""
        Base.metadata.create_all(self.__engine)
        SessionFactory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(SessionFactory)()

    def close(self):
        """Close"""
        self.__session.close()
