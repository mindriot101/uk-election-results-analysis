#!/usr/bin/env python

import sqlite3
import requests
import functools
import models
import argparse
import logging
from tqdm import trange

parser = argparse.ArgumentParser()
parser.add_argument('sqlalchemy_url')
parser.add_argument('-n', '--n-per-page', required=False, default=10, type=int)
parser.add_argument('-v', '--verbose', action='count')
args = parser.parse_args()


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

if args.verbose is not None:
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)


class Client(object):
    def __init__(self):
        self.session = requests.Session()

    def fetch_json(self, url):
        url = self.update_url(url)
        logger.info('sending request to %s', url)
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def update_url(old_url):
        return old_url.replace('http://data', 'http://lda.data')


def get_or_create(session, model, defaults=None, **kwargs):
    ''' Taken from https://stackoverflow.com/a/2587041/56711 '''
    from sqlalchemy.sql.expression import ClauseElement
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


def main():
    engine, Session = models.create_engine_and_session(args.sqlalchemy_url, echo=args.verbose is not None and args.verbose >= 2)
    models.reset_db(engine)
    session = Session()

    page_size = args.n_per_page

    client = Client()
    entries = client.fetch_json('http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}'.format(page_size=page_size))

    total_results = entries['result']['totalResults']
    n_requests = total_results // page_size + 1
    logger.info('Making %s requests', n_requests)

    for request_id in trange(n_requests):
        election_results = client.fetch_json('http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}&_page={request_id}'.format(
            page_size=page_size, request_id=request_id + 1))
        entries = election_results['result']['items']

        for entry in entries:
            # Extract constituency info
            constituency_url = entry['constituency']['_about']
            constituency_info = client.fetch_json(constituency_url + '.json')

            constituency_type = constituency_info['result']['primaryTopic']['constituencyType']
            constituency_name = constituency_info['result']['primaryTopic']['label']['_value']
            constituency_os_name = constituency_info['result']['primaryTopic']['osName']

            constituency_model, _ = get_or_create(session, models.Constituency,
                    type=constituency_type,
                    name=constituency_name,
                    os_name=constituency_os_name)
            session.add(constituency_model)

            # Extract election info

            election_url = entry['_about']
            election_info = client.fetch_json(election_url + '.json')
            turnout = election_info['result']['primaryTopic']['turnout']

            # Extract detailed election info
            detailed_election_url = election_info['result']['primaryTopic']['election']['_about']
            detailed_election_info = client.fetch_json(detailed_election_url + '.json')
            election_type = detailed_election_info['result']['primaryTopic']['electionType']
            election_label = detailed_election_info['result']['primaryTopic']['label']['_value']

            election_model, _ = get_or_create(session, models.Election,
                    type=election_type,
                    label=election_label)
            session.add(election_model)

            turnout_model, _ = get_or_create(session, models.Turnout,
                    election=election_model,
                    constituency=constituency_model,
                    turnout=turnout)
            session.add(turnout_model)

            # Extract candidate info
            candidate_urls = election_info['result']['primaryTopic']['candidate']

            for candidate_url in candidate_urls:
                candidate = client.fetch_json(candidate_url + '.json')

                try:
                    vote_change_percentage = candidate['result']['primaryTopic']['voteChangePercentage']
                except KeyError:
                    vote_change_percentage = None

                votes = candidate['result']['primaryTopic']['numberOfVotes']
                full_name = candidate['result']['primaryTopic']['fullName']['_value']
                party = candidate['result']['primaryTopic']['party']['_value']

                candidate_model, _ = get_or_create(session, models.Candidate,
                        full_name=full_name)

                votes_model, _ = get_or_create(session, models.Votes,
                        constituency=constituency_model,
                        candidate=candidate_model,
                        election=election_model,
                        votes=votes,
                        vote_change_percentage=vote_change_percentage,
                        party=party)

                session.add(votes_model)

            session.commit()

if __name__ == '__main__':
    main()
