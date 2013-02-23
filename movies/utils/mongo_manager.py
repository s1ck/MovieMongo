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
        try:
            if '_id' in film.keys():
                film['modified_at'] = time.time()
            else:
                film['created_at'] = time.time()
            print "=== saving film"
            return self._movie_coll.save(film)
        except:
            print sys.exc_info()[1]
            return None

    def get_film_by_id(self, film_id):
        try:
            return self._movie_coll.find_one({'_id': self.get_object_id(film_id)})
        except:
            print sys.exc_info()[1]
            return None

    def get_films_by_name(self, name):
        try:
            return self._movie_coll.find({'name': name})
        except:
            print sys.exc_info()[1]
            return None

    def get_films_by_pattern(self, pattern):
       try:
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

    def get_films_by_user(self, user_id):
        try:
            user = self._user_coll.find_one({'_id': user_id})
            films = []

            if 'films' in user.keys():
                film_ids = user['films']
                for film_id in film_ids:
                    film = self.get_film_by_id(film_id)
                    films.append(film)
            return films
        except:
            print sys.exc_info()[1]
            return None

    # user methods

    def get_user_by_id(self, user_id):
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
                print "=== user_has_movie: user does not exist", user_id
        except:
            print sys.exc_info()[1]
            return False

    # link methods

    def get_link_by_id(self, link_id):
        try:
            return self._link_coll.find_one({'_id': self.get_object_id(link_id)})
        except:
            print sys.exc_info()[1]
            return None

    def get_links_by_pattern(self, pattern):
       try:
           return self._link_coll.find(pattern)
       except:
           print sys.exc_info()[1]
           return None

    def has_link(self, from_id, to_id):
        exists = False
        # A -> B
        p1 = {'source_film_id':
                self.get_object_id (from_id),
                'target_film_id':
                self.get_object_id (to_id)
                }
        # B -> A
        p2 = {'source_film_id':
                self.get_object_id (to_id),
                'target_film_id':
                self.get_object_id (from_id),
                }

        # check if at least one of the pattern exists
        p1_cursor = self.get_links_by_pattern (p1)
        exists = p1_cursor is None or p1_cursor.count () == 0

        if exists:
            p2_cursor = self.get_links_by_pattern (p2)
            exists = p2_cursor is None or p2_cursor.count () == 0

        return exists

    def upsert_link(self, from_id, to_id):
        try:
            source_film = self.get_film_by_id(from_id)
            target_film = self.get_film_by_id(to_id)
            error = False

            if source_film is None:
                print "=== upsert_link: source film does not exist", from_id
                error = True
            if target_film is None:
                print "=== upsert_link: target film does not exist", to_id
                error = True

            if not error:
                print "=== upsert_link: storing link between %s and %s" % \
                    (source_film['_id'], target_film['_id'])
                return self._link_coll.save({
                    'source_film_id': from_id,
                    'target_film_id': to_id,
                    })
            else:
                return None
        except:
            print sys.exc_info()[1]
            return None

    # user content methods

    def get_usercontent(self, film_id, user_id):
        try:
            return self._ucontent_coll.find({'user_id': user_id, 'film_id': film_id})
        except:
            print sys.exc_info()[1]
            return None

    def upsert_usercontent(self, film_id, user_id, key, value):
        try:
            return self._ucontent_coll.save({
                    "user_id": user_id,
                    "film_id": film_id,
                    "created_at": time.time(),
                    "key": key,
                    "value": value
                    })
        except:
            print sys.exc_info()[1]
            return None

    def remove_usercontent(self, id):
        try:
            return self._ucontent_coll.remove({'_id': self.get_object_id(id)})
        except:
            print sys.exc_info()[1]
            return None

# helpers

    def get_object_id(self, identifier):
        return identifier if isinstance(identifier, ObjectId) \
            else ObjectId(str(identifier))

