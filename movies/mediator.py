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

        # stage 1: store links between movies

        # stage 2: complete documents with data from links

        # stage 3: store non exisiting films in the database
        self.store_films(films['result'])

        # stage 4: get distinct movies
        films['result'] = self.get_distinct_movies(films['result'])

        # some json serialization
        films['result'] = [json.loads(dumps(f)) for f in films['result']]
        return films

    def get_film_by_id(self, film_id, source):
        if source in self._wrappers:
            return self._wrappers[source].get_film_by_id(film_id)
        return None

    def store_links(self, films):
        pass

    def store_films(self, films):
        for film in films:
            # film found in mongodb?
            if '_id' not in film.keys():
                    # film with same name, source and title already stored?
                    pattern = {'name': film['name']
                            ,'initial_release_date':
                            film['initial_release_date']
                            ,'source': film['source']
                            }
                    db_films = self._mongo_mgr.get_films_by_pattern(pattern)
                    if db_films is None or db_films.count() == 0:
                        film['_id'] = self._mongo_mgr.upsert_film(film)
                    else:
                        print ">>>>>>>>>>" , film['name'], ">>>>", film['initial_release_date']
                        # match (p.e. by year) if this is really the same film
                        film['_id'] = db_films[0]['_id']
                        print '=== found movie with same name, skip store'
            else:
                print '=== movie has _id, skip store'

    def get_distinct_movies(self, films):
        # not possible, have to preserve the order
        #return {v['_id']:v for v in films}.values()}
        ret = []
        ids = set()
        for film in films:
            if film['_id'] not in ids:
                ret.append(film)
                ids.add(film['_id'])
        return ret
