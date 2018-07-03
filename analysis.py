#!/usr/bin/env python


from models import (create_engine_and_session,
        Candidate,
        Constituency,
        Election,
        Turnout,
        Votes)
import logging
import argparse


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sqlalchemy_url')
    args = parser.parse_args()

    engine, Session = create_engine_and_session(args.sqlalchemy_url)
    session = Session()

    # Get distinct general elections
    query = session.query(Election.label).filter(Election.type.ilike('%general%'))
    distinct_general_election_names = [row[0] for row in query]

    for election_name in distinct_general_election_names:
        query = session.query(Votes)
        query = query.join(Election).filter(Election.label == election_name)
        break

