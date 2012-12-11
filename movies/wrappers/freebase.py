# -*- coding: utf-8 -*-

import json

from apiclient import discovery

from movies import settings
from movies.wrappers.base import BaseWrapper


class FreebaseWrapper(BaseWrapper):
    
    def __init__(self):
        self.__google_api_key = settings.GOOGLE_API_KEY
        self.__freebase = discovery.build('freebase', 'v1',
                developerKey=settings.GOOGLE_API_KEY)

    def get_name(self):
        return "freebase"

    def get_films_by_name(self, name):
        query = [{
            'name~=': name,  # LIKE "%name"
            'name': None,  # MUST have name
            'type': '/film/film',  # must be of type film
            '*': [],  # any other stuff
            #'genre': None,
            #'initial_release_date': None,
            #'written_by': None,
            #'directed_by': None,
            'starring': [{
                'actor': {'name': None}
            }],
            'key': [{
                'namespace': None,
                'value': None
            }],
        }]
        response = json.loads(self.__freebase
                .mqlread(query=json.dumps(query)).execute())
        return self._normalize(response)

    def _normalize(self, response):
        """maps a query response to the global result schema"""

        # source key: (normalized key, transformation method to call)
        mappings = {
            'name': ('name', None),
            'initial_release_date': ('initial_release_date',
                    self._get_year),
            'directed_by': ('directed_by', None),
            'written_by': ('written_by', None),
            'starring' : ('actors', self._get_actors),
            'genre': ('genre', None),
            'key': ('links', self._get_links),
        }

        mapping_keys = mappings.keys()
        results = []
        for result in response['result']:
            normalized_res = {}
            for key in result:
                if key in mapping_keys:
                    val = result[key]
                    if mappings[key][1] is not None:
                        method = mappings[key][1]
                        val = method(val)
                    normalized_key = mappings[key][0]
                    normalized_res[normalized_key] = val
                    normalized_res['source'] = self.get_name()
            results.append(normalized_res)
        return {'result': results}

    def _get_year(self, date_val):
        """
        :param date_val: sth like this: [u'1979-08-17']
        """
        if len(date_val) == 0:
            return None
        date_str = date_val[0]
        year_str = date_str.split('-', 1)[0]
        year = int(year_str)

        return year

    def _get_actors(self, actor_vals):
        """
        :param actor_vals: sth like this:
        (Pdb) pp(actors_val)
        [{u'actor': {u'name': u'Graham Chapman'}},
         {u'actor': {u'name': u'John Cleese'}},
         {u'actor': {u'name': u'Terry Gilliam'}},
         {u'actor': {u'name': u'Eric Idle'}},
         {u'actor': {u'name': u'Michael Palin'}},
         {u'actor': {u'name': u'Kenneth Colley'}},
         {u'actor': {u'name': u'Graham Chapman'}},
         {u'actor': {u'name': u'Terry Jones'}},
         {u'actor': {u'name': u'John Young'}},
         {u'actor': {u'name': u'Eric Idle'}},
         {u'actor': {u'name': u'Eric Idle'}},
         {u'actor': {u'name': u'John Cleese'}},
         {u'actor': {u'name': u'Terence Bayler'}},
         {u'actor': {u'name': u'Carol Cleveland'}},
         {u'actor': {u'name': u'Neil Innes'}}]
        """
        actors = []
        for actor in actor_vals:
            name = actor['actor']['name']
            actors.append(name)

        return actors
    
    def _get_links(self, link_vals):
        """
        :param link_vals: sth like this:
        (Pdb) pp(response['result'][0]['key'])
        [{u'namespace': u'/wikipedia/en_id', u'value': u'17920'},
         {u'namespace': u'/en', u'value': u'life_of_brian'},
         {u'namespace': u'/authority/imdb/title', u'value': u'tt0079470'},
         {u'namespace': u'/source/traileraddict/movie',
          u'value': u'monty-pythons-life-of-brian'},
         {u'namespace': u'/source/traileraddict/embed', u'value': u'2789'},
         {u'namespace': u'/user/avh/ellerdale', u'value': u'0080-c4e4'},
         {u'namespace': u'/source/metacritic/movie',
          u'value': u'montypythonslifeofbrian'},
         {u'namespace': u'/source/videosurf', u'value': u'18224'},
         {u'namespace': u'/wikipedia/de_id', u'value': u'31512'},
         ...
        ]
        """
        # TODO: do sth useful here
        return link_vals

