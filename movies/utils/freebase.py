import json

from apiclient import discovery


class FreebaseWrapper(object):
    def __init__(self, google_api_key):
        self.__google_api_key = google_api_key
        self.__freebase = discovery.build('freebase', 'v1',
                developerKey=google_api_key)

    def get_film_by_name(self, name):
        query = [{'name~=': name, # LIKE "%name"
                  'name': None, # MUST have name
                  'type': '/film/film', # must be of type film
                  '*': [], # any other stuff
                  }]
        response = json.loads(self.__freebase
                .mqlread(query=json.dumps(query))
                .execute())

        return response
