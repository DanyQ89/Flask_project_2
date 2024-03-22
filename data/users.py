import datetime

from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String)
    age = Column(Integer)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    city_from = Column(String)
    modified_date = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return (f'{self.surname} {self.name} {self.age} {self.position} {self.speciality}'
                f'\n{self.address} {self.email} {self.hashed_password}')
