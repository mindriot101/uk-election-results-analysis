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

    query = session.query(Votes)
    query = query.join(Election).filter(Election.type.ilike('%general%'))
    print(query.first())

