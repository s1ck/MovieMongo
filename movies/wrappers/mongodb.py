# -*- coding: utf-8 -*-
import pymongo
import re

from base import BaseWrapper

class MongoDBWrapper(BaseWrapper):

    def __init__(self, host, port):
        self.__connection = pymongo.MongoClient(host=host, port=port)
        self.__db = self.__connection.wcm12

    def get_name(self):
        return "mongodb"

    def get_films_by_name(self, name):
        films = {}
        films['result'] = []
        regex = re.compile(name, re.IGNORECASE)
        mongo_result = self.__db.movie.find({'titles': {'$in':[regex]}})
        for doc in mongo_result:
            films['result'].append(self.normalize(doc))
        return films

    def get_film_by_id(self, film_id):
        return self.__db.movie.find_one({'_id': film_id})


    def normalize(self, film):
        # select first embedded document which is already normalized to the
        # global schema
        film_id = film['_id']
        film = film['data'][0].values()[0]
        film['id'] = film_id
        film['source'] = self.get_name()
        return film

