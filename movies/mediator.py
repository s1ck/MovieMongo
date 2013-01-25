# -*- coding: utf-8 -*-

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

    def store_films(self, films):
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
                    film['_id'] = self._mongo_mgr.upsert_film(film)
                else:
                    # match (p.e. by year) if this is really the same film
                    film['_id'] = db_films[0]['_id']
                    print('=== found movie with same name, skip store')
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
                            ,'genre': None
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
                link['oid'] = to_film['_id']

                # search the link collection if a link exists in one of the
                # both possible directions
                if not self._mongo_mgr.has_link (from_id, to_film['_id']):
                    self._mongo_mgr.upsert_link (from_id, to_film['_id'])

            # store updated links
            self._mongo_mgr.upsert_film (from_film)

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
