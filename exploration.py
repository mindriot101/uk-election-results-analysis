#!/usr/bin/env python

import sqlite3
import requests
import functools

def fetch_json(url):
    url = update_url(url)
    print(url)
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def update_url(old_url):
    return old_url.replace('http://data', 'http://lda.data')


def get(obj, *keys):
    return functools.reduce(lambda obj, key: obj[key], keys, obj)


# TODO: up this
page_size = 1 

entries = fetch_json(f'http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}')

total_results = get(entries, 'result', 'totalResults')
n_requests = total_results // page_size + 1
print(f'Making {n_requests} requests')

for request_id in range(n_requests):
    result = fetch_json(f'http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}&_page={request_id + 1}')
    entries = get(result, 'result', 'items')
    for entry in entries:
        constituency = get(entry, 'constituency', 'label', '_value')
        election_label = get(entry, 'election', 'label', '_value')

        about_link = entry['_about'] + '.json'
        details = fetch_json(about_link)
        candidates = get(details, 'result', 'primaryTopic', 'candidate')

        for candidate_url in candidates:
            url = candidate_url + '.json'
            candidate = fetch_json(url)

            break

        break

    break
