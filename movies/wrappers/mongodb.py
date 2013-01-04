# -*- coding: utf-8 -*-
import pymongo
import re

from base import BaseWrapper

class MongoDBWrapper(BaseWrapper):

    def __init__(self, mongo_mgr):
        self._mongo_mgr = mongo_mgr

    def get_name(self):
        return "mongodb"

    def get_films_by_name(self, name):
        films = {}
        films['result'] = []
        mongo_result = self._mongo_mgr.get_films_by_regex('name', name)
        if mongo_result is not None:
            for doc in mongo_result:
                films['result'].append(doc)
        return films

    def get_film_by_id(self, film_id):
        return self._mongo_mgr.get_film_by_id(film_id)
