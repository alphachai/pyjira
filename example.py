#!/usr/bin/env python3

from collections import defaultdict
from getpass import getpass

from client.requests import IssueSearch, Issue

username = input('Atlassian Username: ')
password = getpass('Password for {}: '.format(username))

query = 'project = MOAT and component in ("Survey System", "Custom Databases") and status in ("Planned", "In Progress", "Code Review", "On Hold") and type not in ("Epic") ORDER BY updated DESC',

request = IssueSearch(
    auth=(username, password),
    query=query,
)

request.execute()

results = defaultdict(list)

for issue in request.response:
    results[issue.status].append(issue)

for status, issues in results.items():
    print(status)
    for i in issues:
        print(i)

