import json

from apiclient import discovery

from movies import settings

class FreebaseWrapper(object):
    def __init__(self):
        self.__google_api_key = settings.GOOGLE_API_KEY
        self.__freebase = discovery.build('freebase', 'v1',
                developerKey=settings.GOOGLE_API_KEY)

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
