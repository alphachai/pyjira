#!/usr/bin/env python3

import requests


class DesiredKeyNotFound(Exception):
    pass


class RequiredParameterUndefined(Exception):
    pass


class JiraRequest(object):
    # https://docs.atlassian.com/jira/REST/cloud/
    base_url = None
    endpoint = None
    url = None
    auth = None
    payload = None
    _response = None
    _desired_objects = None

    def __init__(self, auth=None, payload=None):
        self.auth = auth
        self.payload = payload
        self.url = self.build_url()

    def build_url(self):
        if self.base_url and self.endpoint:
            return '{}/{}'.format(self.base_url, self.endpoint)
        else:
            raise RequiredParameterUndefined('base_url, endpoint')

    def fetch(self, start_at=None):
        if start_at:
            self.payload['startAt'] = start_at
        r = requests.get(self.url, auth=self.auth, params=self.payload)
        if not r.raise_for_status():
            return r.json()

    def find_desired_objs(self, r):
        if self._desired_objects:
            if self._desired_objects in r:
                return r[self._desired_objects]
            else:
                raise DesiredKeyNotFound('Did not find {} in the response.'.format(self._desired_objects))
        else:
            return r

    def execute(self):
        if not self._response and self.payload and self.auth:
            print(self.url)
            datum = []
            start_at = 0
            self.show_progress(20, 0, 100)
            r = self.fetch()
            datum.extend(self.find_desired_objs(r))
            try:
                while r['startAt'] + r['maxResults'] < r['total']:
                    start_at = r['startAt'] + r['maxResults']
                    self.show_progress(20, start_at, r['total'])
                    r = self.fetch(start_at)
                    datum.extend(self.find_desired_objs(r))
                self.show_progress(20, 1, 1)
                self._response = datum
            except Exception as e:
                raise

    def _make_progress_bar(self, length, x, n):
        """ Return progress bar string.

        Args:
            length (int): Length of the pipe that will be displayed.
            n (int): Progress numeratorl
            total (int): Progress denominator;
        """
        done = '#' * int(length * (x / n))
        todo = '-' * int(length * (1 - (x / n)))
        progress = int((x / n) * 100)
        return '<{}> {}%           '.format(done + todo, progress)

    def show_progress(self, length, x, n):
        progress = int((x / n) * 100)
        s = self._make_progress_bar(length, x, n)
        if progress >= 100:
            end = '\n'
        else:
            end = '\r'

        print('{}'.format(s), end=end)

    @property
    def response(self):
        return self._response


class IssueSearch(JiraRequest):
    base_url = 'https://mintel.atlassian.net/rest/api/2'
    endpoint = 'search'
    _desired_objects = 'issues'


    @property
    def response(self):
        issues = []
        for i in self._response:
            new_issue = Issue(i['id'], i['key'], i['fields']['summary'], i['fields'])
            issues.append(new_issue)
        return issues


class Issue(object):
    def __init__(self, id, key, title, fields):
        self.id = id
        self.key = key
        self.title = title
        self.fields = fields

    def __str__(self):
        return '{} - {}'.format(self.key, self.title)

