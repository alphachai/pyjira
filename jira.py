#! /usr/bin/python

import os
import pwd
import requests
from getpass import getpass


class JiraSearchRequest(object):
    # https://docs.atlassian.com/jira/REST/cloud/ 
    base_url = 'https://mintel.atlassian.net/rest/api/2'
    endpoint = 'search'
    url = None
    auth = None
    payload = None
    response = None

    def __init__(self, auth=None, payload=None):
        self.auth = auth
        self.payload = payload
        self.url = self.build_url()

    def build_url(self):
        return '{0}/{1}'.format(self.base_url, self.endpoint)

    def fetch(self, start_at=None):
        if start_at:
            self.payload['startAt'] = start_at
        r = requests.get(self.url, auth=self.auth, params=self.payload)
        if not r.raise_for_status():
            return r.json()

    def execute(self):
        if not self.response and self.payload and self.auth:
            print self.url
            issues = []
            start_at = 0
            r = self.fetch()
            issues.extend(r['issues'])
            while r['startAt'] +  r['maxResults'] < r['total']:
                start_at = r['startAt'] + r['maxResults']
                r = self.fetch(start_at)
                issues.extend(r['issues'])
            self.response = issues

username = '{0}@mintel.com'.format(pwd.getpwuid(os.getuid()).pw_name)
password = getpass('Password for {0}: '.format(username))

payload = {
    'jql': 'project = MOAT and component in ("Survey System", "Custom Databases") and status in ("Planned", "In Progress", "Code Review", "On Hold") and type not in ("Epic") ORDER BY updated DESC',
}

request = JiraSearchRequest(
    auth=(username, password),
    payload=payload,
)

request.execute()

for i in request.response:
    print '{0} - {1}'.format(i['key'], i['fields']['summary'])
