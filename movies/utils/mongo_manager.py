# -*- coding: utf-8 -*
import re
import sys
import time

import pymongo
from bson.objectid import ObjectId


class MongoManager(object):
    def __init__(self, host, port):
        self._c = pymongo.MongoClient(host, port)
        self._movie_coll = self._c.wcm12.movie
        self._link_coll = self._c.wcm12.link
        self._user_coll = self._c.wcm12.user
        self._ucontent_coll = self._c.wcm12.usercontent

    # film methods

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
        print self._movie_coll
        try:
            return self._movie_coll.find_one({'_id': self.get_object_id(film_id)})
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

    def get_films_by_pattern(self, pattern):
       try:
           print "=== get_films_by_pattern(", pattern, ")"
           return self._movie_coll.find(pattern)
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

    # user methods

    def get_user_by_id(self, user_id):
        print self._user_coll
        try:
            return self._user_coll.find_one({'_id': user_id})
        except:
            print sys.exc_info()[1]
            return None

    def add_film_to_user(self, film_id, user_id):
        try:
            user = self.get_user_by_id(user_id)
            film = self.get_film_by_id(film_id)

            if user and film:
                if 'films' not in user.keys():
                    user['films'] = [film['_id']]
                else:
                    user['films'] += [film['_id']]
                self._user_coll.save(user)
            else:
                print "=== add_film_to_user: user or film was None"
        except:
            print sys.exc_info()[1]

    def remove_film_from_user(self, film_id, user_id):
        try:
            user = self.get_user_by_id(user_id)
            film_id = self.get_object_id(film_id)

            if user and film_id:
                if 'films' in user.keys() and film_id in user['films']:
                    user['films'].remove(film_id)
                    self._user_coll.save(user)
            else:
                print "=== remove_film_from_user: user of film was None"
        except:
            print sys.exc_info()[1]

    def user_has_movie(self, film_id, user_id):
        try:
            user = self.get_user_by_id(user_id)
            if user and 'films' in user:
                return (self.get_object_id(film_id) in user['films'])
            else:
                print "=== user_has_movie: user does not exist"
        except:
            print sys.exc_info()[1]
            return False


    # helpers

    def get_object_id(self, identifier):
        return identifier if isinstance(identifier, ObjectId) \
            else ObjectId(str(identifier))

