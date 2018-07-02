from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint


Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False, unique=True)


class Constituency(Base):
    __tablename__ = 'constituencies'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    os_name = Column(String, nullable=False)


class Election(Base):
    __tablename__ = 'elections'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    label = Column(String, nullable=False, unique=True)


class Turnout(Base):
    __tablename__ = 'turnouts'

    id = Column(Integer, primary_key=True)
    turnout = Column(Integer, nullable=False)

    # Foreign keys
    election_id = Column(Integer, ForeignKey('elections.id'),
            nullable=False)
    constituency_id = Column(Integer, ForeignKey('constituencies.id'),
            nullable=False)

    # Relationships

    election = relationship('Election')
    constituency = relationship('Constituency')

    # Constraints

    __table_args__ = (
            UniqueConstraint('election_id', 'constituency_id'),
            )


class Votes(Base):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)
    votes = Column(Integer, nullable=False)
    vote_change_percentage = Column(Float, nullable=True)
    party = Column(String, nullable=False)

    # Foreign keys
    candidate_id = Column(Integer, ForeignKey('candidates.id'),
            nullable=False)
    constituency_id = Column(Integer, ForeignKey('constituencies.id'),
            nullable=False)
    election_id = Column(Integer, ForeignKey('elections.id'),
            nullable=False)

    # Relationships

    candidate = relationship('Candidate')
    constituency = relationship('Constituency')
    election = relationship('Election')

    # Constraints

    __table_args__ = (
            UniqueConstraint('candidate_id', 'constituency_id',
                'election_id'),
            )


def reset_db(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def create_engine_and_session(connect_url, *args, **kwargs):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(connect_url, *args, **kwargs)
    Session = sessionmaker(bind=engine)

    return engine, Session
