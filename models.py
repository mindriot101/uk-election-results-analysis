from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)


class Constituency(Base):
    __tablename__ = 'constituencies'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    os_name = Column(String, nullable=False)


class Election(Base):
    __tablename__ = 'elections'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    label = Column(String, nullable=False)


class Turnout(Base):
    __tablename__ = 'turnouts'

    id = Column(Integer, primary_key=True)
    turnout = Column(Integer, nullable=False)
    election_id = Column(Integer, ForeignKey('elections.id'))
    constituency_id = Column(Integer, ForeignKey('constituencies.id'))


class Votes(Base):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)
    votes = Column(Integer, nullable=False)
    vote_change_percentage = Column(Float, nullable=True)
    party = Column(String, nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    constituency_id = Column(Integer, ForeignKey('constituencies.id'))
    election_id = Column(Integer, ForeignKey('elections.id'))
