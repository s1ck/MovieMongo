# -*- coding: utf-8 -*-

from bson.json_util import dumps
import time
import json


class Mediator(object):
    def __init__(self, mongo_mgr):
        self._mongo_mgr = mongo_mgr
        self._wrappers = {}

        self._c_interv = int (mongo_mgr.get_property
                ('cache_invalidation_interval'))

    def add_wrapper(self, wrapper):
        self._wrappers[wrapper.get_name()] = wrapper

    def get_wrapper(self, wrapper_name):
        if wrapper_name in self._wrappers.keys ():
            return self._wrappers[wrapper_name]
        else:
            return None

    def get_films_by_name(self, name):
        now = int(time.time())
        films = {}
        films['result'] = []
        exclusion = {}

        # exclude already existing films from search
        if 'mongodb' in self._wrappers.keys():
            mongo_wrapper = self._wrappers['mongodb']
            films['result'] += mongo_wrapper.get_films_by_name (name)['result']
            for film in films['result']:
                # exclude films from search which have been lately collected
                if (now - film['modified_at']) < self._c_interv:
                    if film['source'] not in exclusion.keys ():
                        exclusion[film['source']] = [film['source_id']]
                    else:
                        exclusion[film['source']].append (film['source_id'])

        for k,v in self._wrappers.iteritems ():
            if k is not 'mongodb':
                if k not in exclusion.keys ():
                    films['result'] += v.get_films_by_name (name)['result']
                else:
                    films['result'] += v.get_films_by_name (name,
                            exclusion[k])['result']

        # stage 1: store non exisiting films in the database
        self.store_films(films['result'], now)

        # stage 2: get distinct movies
        films['result'] = self.get_distinct_movies(films['result'])

        # stage 3: store new links between movies
        self.store_links(films['result'])

        # stage 3: complete documents with data from links

        # some json serialization
        films['result'] = [json.loads(dumps(f)) for f in films['result']]
        return films

    def get_film_by_id(self, film_id, source):
        if source in self._wrappers:
            return self._wrappers[source].get_film_by_id(film_id)
        return None

    def store_films(self, films, now):
        '''
        checks if the found films exist in the database using their name,
        initial_release_date and the source attribute to guarantee uniqueness.

        if the film doesn't exist, it is saved and updated with the generated
        _id attribute.
        '''
        for film in films:
            # film found in mongodb?
            if '_id' not in film.keys():
                # film with same name, source and title already stored?
                pattern = {
                    'name': film['name'],
                    'initial_release_date': film['initial_release_date'],
                    'source': film['source']
                }
                db_films = self._mongo_mgr.get_films_by_pattern(pattern)
                if db_films is None or db_films.count() == 0:
                    # film not found, store it
                    film['_id'] = self._mongo_mgr.upsert_film(film)
                else:
                    # film has been found, check if it has to be updated
                    persistent_film = db_films[0]
                    film['_id'] = persistent_film['_id']
                    if (now - persistent_film['modified_at']) > self._c_interv:
                        # update cache and rescue the links if exist
                        if 'links' in persistent_film.keys ():
                            film['links'] = persistent_film['links']
                        self._mongo_mgr.upsert_film (film)
                        print '=== cache updated'
            else:
                print('=== movie has _id, skip store')

    def store_links(self, films):
        for film in films:
            self.store_link(film)

    def store_link(self, from_film):
        '''
        Stores links between films. The links between films are undirected, so
        before a link is stored, it has to be checked if there is a link in the
        opposite direction already stored in the db.
        '''
        from_id = from_film['_id']
        from_source = from_film['source']
        from_source_id = from_film['source_id']
        update_from_film = False

        if 'links' in from_film:
            for link in from_film['links']:
                # try to get linked movie
                to_films = self._mongo_mgr.get_films_by_pattern ({'source_id':
                    link['value']})

                if to_films.count() == 0:
                    # create placeholder film
                    new_film = {'source': link['target']
                            ,'source_id': link['value']
                            ,'name': None
                            ,'initial_release_date': None
                            ,'genre': []
                            ,'directed_by': []
                            ,'written_by': []
                            ,'actors': []
                            ,'img_url': None}
                    new_id = self._mongo_mgr.upsert_film (new_film)
                    new_film['_id'] = new_id
                    # set the new film as target
                    to_film = new_film
                else:
                    # take the existing one
                    to_film = to_films[0]

                # store backward links
                backward_edge = {'target': from_source
                        ,'value': from_source_id
                        ,'oid': from_id}

                # if the to_film already has links, check if this one already
                # exists, if not add it or create new links
                update_to_film = False
                if 'links' in to_film.keys ():
                    exists = False
                    for link in to_film['links']:
                        if link['oid'] == from_id:
                            exists = True
                    if not exists:
                        to_film['links'].append (backward_edge)
                        update_to_film = True
                else:
                    to_film['links'] = [backward_edge]
                    update_to_film = True

                if update_to_film:
                    self._mongo_mgr.upsert_film (to_film)

                # update the link with the oid
                if 'oid' not in link.keys ():
                    link['oid'] = to_film['_id']
                    update_from_film = True

                # search the link collection if a link exists in one of the
                # both possible directions
                if not self._mongo_mgr.has_link (from_id, to_film['_id']):
                    self._mongo_mgr.upsert_link (from_id, to_film['_id'])

            # store updated links
            if update_from_film:
                self._mongo_mgr.upsert_film (from_film)

    def update_template_film (self, film):
        '''
        Tries to get the full information of the template film using the source
        information. If the full information could be retrieved, the template
        film will be updated in the database.

        If the full information could not be retrieved, the template film is
        returned.
        '''
        wrapper = self.get_wrapper (film['source'])
        if not wrapper:
            print "No wrapper found for:", film['source']
            return film
        else:
            result = wrapper.get_film_by_id (film['source_id'])
            if result and len (result['result']) > 0:
                remote_film = result['result'][0]
                remote_film['_id'] = film['_id']
                remote_film['links'] = film['links']
                self._mongo_mgr.upsert_film (remote_film)
                return remote_film
            else:
                print "No film found at %s with id %s" % (film['source'],
                        film['source_id'])
                return film

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
