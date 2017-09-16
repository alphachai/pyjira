#!/usr/bin/env python3

import os
import pwd
from getpass import getpass

from client.requests import IssueSearch

#username = '{0}@mintel.com'.format(pwd.getpwuid(os.getuid()).pw_name)
#username = 'cmathews@mintel.com'
username = input('Atlassian Username: ')
password = getpass('Password for {}: '.format(username))

payload = {
    'jql': 'project = MOAT and component in ("Survey System", "Custom Databases") and status in ("Planned", "In Progress", "Code Review", "On Hold") and type not in ("Epic") ORDER BY updated DESC',
    #'jql': 'project = MOAT and status not in ("Done", "Closed")',
}

request = IssueSearch(
    auth=(username, password),
    payload=payload,
)

request.execute()

for i in request.response:
    print(i)

#import pdb; pdb.set_trace()

