#!/usr/bin/env python

import sqlite3
import requests
import functools


class Client(object):
    def __init__(self, verbose=False):
        self.session = requests.Session()
        self.verbose = verbose

    def fetch_json(self, url):
        url = self.update_url(url)
        if self.verbose:
            print(url)
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def update_url(old_url):
        return old_url.replace('http://data', 'http://lda.data')


page_size = 50

client = Client(verbose=True)
entries = client.fetch_json(f'http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}')

total_results = entries['result']['totalResults']
n_requests = total_results // page_size + 1
print(f'Making {n_requests} requests')

for request_id in range(n_requests):
    election_results = client.fetch_json(f'http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}&_page={request_id + 1}')
    entries = election_results['result']['items']
    for entry in entries:
        # Extract constituency info
        constituency_url = entry['constituency']['_about']
        constituency_info = client.fetch_json(constituency_url + '.json')

        constituency_type = constituency_info['result']['primaryTopic']['constituencyType']
        constituency_name = constituency_info['result']['primaryTopic']['label']['_value']
        constituency_os_name = constituency_info['result']['primaryTopic']['osName']

        # Extract election info

        election_url = entry['_about']
        election_info = client.fetch_json(election_url + '.json')
        turnout = election_info['result']['primaryTopic']['turnout']

        # Extract detailed election info
        detailed_election_url = election_info['result']['primaryTopic']['election']['_about']
        detailed_election_info = client.fetch_json(detailed_election_url + '.json')
        election_type = detailed_election_info['result']['primaryTopic']['electionType']
        election_label = detailed_election_info['result']['primaryTopic']['label']['_value']

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

            break

        break

    break
