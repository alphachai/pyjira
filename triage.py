#!/usr/bin/env python3

import os
import pwd
from collections import defaultdict
from getpass import getpass

from client.requests import IssueSearch, Issue

#username = '{0}@mintel.com'.format(pwd.getpwuid(os.getuid()).pw_name)
username = input('Atlassian Username: ')
password = getpass('Password for {}: '.format(username))

#query = 'project = MOAT and component in ("Survey System", "Custom Databases") and status in ("Planned", "In Progress", "Code Review", "On Hold") and type not in ("Epic") ORDER BY updated DESC',
query = 'createdDate > -1d and project = MOAT and status in ("Incoming", "Triaged") and assignee = it-dev-maintenance-operations'

request = IssueSearch(
    auth=(username, password),
    query=query,
)

request.execute()

results = defaultdict(list)

for issue in request.response:
    component = "Unknown"
    if len(issue.components) > 0:
        component = issue.components[0]
    results[component].append(issue)

for component, issues in results.items():
    print(component)
    for i in issues:
        print(i)

import pdb; pdb.set_trace()
