import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    chief = Column(Integer, ForeignKey('users.id'))
    members = Column(String)
    email = Column(String)