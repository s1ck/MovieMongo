# -*- coding: utf-8 -*-
import pymongo
from bson.json_util import dumps
import json

class Mediator(object):
    def __init__(self, mongo_mgr):
        self._mongo_mgr = mongo_mgr
        self._wrappers = {}

    def add_wrapper(self, wrapper):
        self._wrappers[wrapper.get_name()] = wrapper

    def get_films_by_name(self, name):
        films = {}
        films['result'] = []

        for wrapper in self._wrappers.values():
            films['result'] += wrapper.get_films_by_name(name)['result']

        # stage 1: store non exisiting films in the database
        self.store_films(films['result'])

        # some json serialization
        films['result'] = [json.loads(dumps(f)) for f in films['result']]
        return films

    def get_film_by_id(self, film_id, source):
        if source in self._wrappers:
            return self._wrappers[source].get_film_by_id(film_id)
        return None

    def store_films(self, films):
        for film in films:
            # film found in mongodb?
            if '_id' not in film.keys():
                    # film with same name already stored?
                    db_films = self._mongo_mgr.get_films_by_name(film['name'])
                    if db_films is None or db_films.count() == 0:
                        self._mongo_mgr.upsert_film(film)
                    else:
                        # match (p.e. by year) if this is really the same film
                        print '=== found movie with same name, skip store'
            else:
                print '=== movie has _id, skip store'







