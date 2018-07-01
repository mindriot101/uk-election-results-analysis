#!/usr/bin/env python

import sqlite3
import requests

def fetch_json(url):
    url = update_url(url)
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def update_url(old_url):
    return old_url.replace('http://data', 'http://lda.data')


page_size = 50
entries = fetch_json(f'http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}')

total_results = entries['result']['totalResults']
n_requests = total_results // page_size + 1
print(f'Making {n_requests} requests')

for request_id in range(n_requests):
    result = fetch_json(f'http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}')
    entries = result['result']['items']
    for entry in entries:
        constituency = entry['constituency']['label']['_value']
        election_label = entry['election']['label']['_value']

        about_link = entry['_about'] + '.json'
        details = fetch_json(about_link)
        candidates = details['result']['primaryTopic']['candidate']

        for candidate in candidates:
            url = candidate + '.json'
            print(url)

        break

    break
