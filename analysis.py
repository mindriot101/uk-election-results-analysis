#!/usr/bin/env python


from models import (create_engine_and_session,
        Candidate,
        Constituency,
        Election,
        Turnout,
        Votes)
from sqlalchemy.sql import func
import logging
import argparse


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def top_voted_for(session):
    query = session.query(Candidate).join(Votes).join(Election).join(Constituency)
    query = query.order_by(Votes.votes.desc())
    query = query.limit(10)
    query = query.with_entities(
            Candidate.full_name, Votes.votes, Election.label, Constituency.name)
    logger.info('QUERY: \n%s\n', query)

    for name, votes, election, constituency in query:
        print(name, votes, election, constituency)


def coventry_history(session):
    query = session.query(Constituency).filter(Constituency.name.ilike('%coventry%'))
    query = query.join(Votes).join(Election)
    query = query.filter(Election.type.ilike('%general%'))
    query = query.group_by(Constituency, Election)
    query = query.with_entities(
            func.sum(Votes.votes), Election.label, Constituency.name)
    logger.info('QUERY: \n%s\n', query)

    for votes, election, name in query:
        print(votes, election, name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sqlalchemy_url')
    args = parser.parse_args()

    engine, Session = create_engine_and_session(args.sqlalchemy_url)
    session = Session()

    # top_voted_for(session)
    coventry_history(session)

