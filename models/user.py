#!/usr/bin/python3
""" holds class User"""
from hashlib import md5
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self.password = self._hash_password(kwargs.get('password'))

    @property
    def password(self):
        """Gets the password (hashed)"""
        return self._password

    @password.setter
    def password_h(self, value):
        """Sets and hashes the password"""
        self._password = self.hash_password(value)


    def password_hash(self, password):
        '''password'''
        return hashlib.md5(password.encode()).hexdigest()

    def to_dict(self, include_password=False):
        """Converts instance into dict format"""
        user_dict = super().to_dict(include_password=include_password)
        return user_dict
