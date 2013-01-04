# -*- coding: utf-8 -*
import re
import sys
import time

import pymongo


class MongoManager(object):
    def __init__(self, host, port):
        self._c = pymongo.MongoClient(host, port)
        self._movie_coll = self._c.wcm12.movie
        self._link_coll = self._c.wcm12.link
        self._user_coll = self._c.wcm12.user
        self._ucontent_coll = self._c.wcm12.usercontent

    def upsert_film(self, film):
        """
        if the film already has an '_id' the corresponding document will be
        updated. if not, a new one will be created

        returns the _id of the saved film
        """
        print '=== upsert_film(', film['name'], ')'
        try:
            if '_id' in film.keys():
                film['modified_at'] = time.time()
            else:
                film['created_at'] = time.time()
            return self._movie_coll.save(film)
        except:
            print sys.exc_info()[1]
            return None

    def get_film_by_id(self, film_id):
        try:
            return self._movie_coll.find_one({'_id': film_id})
        except:
            print sys.exc_info()[1]
            return None

    def get_films_by_name(self, name):
        try:
            print "=== get_films_by_name(", name, ")"
            return self._movie_coll.find({'name': name})
        except:
            print sys.exc_info()[1]
            return None

    def get_films_by_regex(self, attr_key, attr_value):
        try:
            regex = re.compile(attr_value, re.IGNORECASE)
            return self._movie_coll.find({attr_key: regex})
        except:
            print sys.exc_info()[1]
            return None
