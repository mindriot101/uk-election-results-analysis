#!/usr/bin/env python

import sqlite3
import requests


page_size = 50
r = requests.get(f'http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}')
r.raise_for_status()
entries = r.json()

total_results = entries['result']['totalResults']
n_requests = total_results // page_size + 1
print(f'Making {n_requests} requests')

for request_id in range(n_requests):
    r = requests.get(f'http://lda.data.parliament.uk/electionresults.json?_pageSize={page_size}&_page={request_id + 1}')
    r.raise_for_status()
    result = r.json()
    entries = result['result']['items']
    for entry in entries:
        constituency = entry['constituency']['label']['_value']
        election_label = entry['election']['label']['_value']

        about_link = entry['_about'].replace('http://data', 'http://lda.data') + '.json'
        r = requests.get(about_link)
        r.raise_for_status()
        details = r.json()
        print(details)
        break

# {'_about': 'http://data.parliament.uk/resources/382488', 'constituency':
#         {'_about': 'http://data.parliament.uk/resources/145716', 'label': {'_value':
#             'Orkney and Shetland'}}, 'election': {'_about':
#                 'http://data.parliament.uk/resources/382037', 'label': {'_value': '2010
# General Election'}}, 'electorate': 33085, 'majority': 9928, 'resultOfElection':
#                 'LD Hold', 'turnout': 19346}

    break
