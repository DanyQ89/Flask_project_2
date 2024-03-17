import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, Boolean

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader: Column[int] = Column(Integer, sqlalchemy.ForeignKey('users.id'))
    job = Column(String)
    work_size = Column(Integer)
    collaborators = Column(String)
    hazard = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_finished = Column(Boolean)

    def __repr__(self):
        return f'{self.team_leader} {self.job} {self.work_size} {self.collaborators} {self.is_finished}'


