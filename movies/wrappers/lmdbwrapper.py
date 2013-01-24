# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON

from movies.wrappers.base import BaseWrapper


class LMDBWrapper(BaseWrapper):

    def __init__(self):
        self.name = 'lmdb'
        self.endpoint = SPARQLWrapper('http://data.linkedmdb.org/sparql')
        self.endpoint.setReturnFormat(JSON)

        # query to get movie resources
        self.query_movie = '''SELECT *
        WHERE {?movie <http://purl.org/dc/terms/title> '%s'.}'''

        # query to get the title of a movie resource
        self.query_title = '''SELECT ?title
        WHERE {<%s> <http://purl.org/dc/terms/title> ?title.}'''

        # query to get the release date of a movie resource
        self.query_release_date = '''SELECT ?release_date
        WHERE {<%s> <http://data.linkedmdb.org/resource/movie/initial_release_date> ?release_date.}'''

        # query to get the director resource of a movie resource
        self.query_director = '''SELECT ?director
        WHERE {<%s> <http://data.linkedmdb.org/resource/movie/director> ?director.}'''

        # query to get the director name of a director resource
        self.query_director_name = '''SELECT ?director_name
        WHERE {<%s> <http://data.linkedmdb.org/resource/movie/director_name> ?director_name.}'''

        # query to get the writer resource of a movie resource
        self.query_writer = '''SELECT ?writer
        WHERE {<%s> <http://data.linkedmdb.org/resource/movie/writer> ?writer.}'''

        # query to get the name of a writer resource
        self.query_writer_name = '''SELECT ?writer_name
        WHERE {<%s> <http://data.linkedmdb.org/resource/movie/writer_name> ?writer_name.}'''

        # query to get an actor resource of a movie resource
        self.query_actor = '''SELECT ?actor
        WHERE {<%s> <http://data.linkedmdb.org/resource/movie/actor> ?actor.}'''

        # query to get the name of an actor resource
        self.query_actor_name = '''SELECT ?actor_name
        WHERE {<%s> <http://data.linkedmdb.org/resource/movie/actor_name> ?actor_name.}'''

        # query to get a genre resource of a movie resource
        self.query_genre = '''SELECT ?genre
        WHERE {<%s> <http://http://data.linkedmdb.org/resource/movie/film_genre> ?genre.}'''

        # query to get a sameAs link uri of a movie resource
        self.query_sameAs = '''
        SELECT ?sameAs
        WHERE {<%s> <http://www.w3.org/2002/07/owl#sameAs> ?sameAs.}'''

    def get_name(self):
        return self.name

    def get_film_by_id(self, film_id):
        movie = self._query_movie_data(film_id)
        return movie

    def get_films_by_name(self, name):

        # get movie resources via SPARQL query
        self.endpoint.setQuery(self.query_movie % name)
        sparql_res = self.endpoint.query().convert()

        movies = []
        for res in sparql_res['results']['bindings']:
            # res looks sth like this:
            # {u'movie': {
            #     u'type': u'uri',
            #     u'value': u'http://data.linkedmdb.org/resource/film/94307'}
            # }
            uri = res['movie']['value']
            movie = self._query_movie_data(uri)
            movies.append(movie)

        return {'result': movies}

    def _query_movie_data(self, uri):
        # get title
        title = self._query_title(uri)
        # get year
        year = self._query_year(uri)
        # get director
        directors = self._query_director(uri)
        # get writer
        writers = self._query_writers(uri)
        # get actors
        actors = self._query_actors(uri)
        ### there are currently no genres set in lmdb
        ### # get genres
        ### genres = self._query_genres(uri)

        movie = {
            'name': title,
            'initial_release_date': year,
            'directed_by': directors,
            'written_by': writers,
            'actors': actors,
            'source': self.name,
            'source_id': uri,
            'genre': []
        }

        links = self._query_sameAs(uri)
        if links is not None and len(links) > 0:
            movie['links'] = []
            for link in links:
                movie['links'].append(link)
        return movie

    def _query_title(self, uri):
        self.endpoint.setQuery(self.query_title % uri)
        sparql_res = self.endpoint.query().convert()

        bindings = sparql_res['results']['bindings']
        if len(bindings) > 0:
            # standard case: movie has one title
            # if it has more than one title I will ignore all except the
            # first one
            # TODO: handle multi-titled movies
            title = bindings[0]['title']['value']
            return title
        else:
            # strange case: movie has no title
            return None

    def _query_year(self, uri):
        self.endpoint.setQuery(self.query_release_date % uri)
        sparql_res = self.endpoint.query().convert()

        bindings = sparql_res['results']['bindings']
        if len(bindings) > 0:
            # standard case: movie has exactly one release year
            # if it has more than one release year I will ingnore all except
            # the first one
            # TODO: handle multiple initial release years
            release_date = bindings[0]['release_date']['value']

            # since release_date can be just an integer like '1984' but also a
            # date string like '2006-09-01' I will take this shot from the hip
            year = int(release_date.split('-')[0])

            return year
        else:
            return None

    def _query_director(self, uri):
        self.endpoint.setQuery(self.query_director % uri)
        sparql_res = self.endpoint.query().convert()

        directors = []
        bindings = sparql_res['results']['bindings']
        for binding in bindings:
            director_uri = binding['director']['value']
            director_name = self._query_director_name(director_uri)
            if director_name is not None:
                directors.append(director_name)
        return directors

    def _query_director_name(self, uri):
        self.endpoint.setQuery(self.query_director_name % uri)
        sparql_res = self.endpoint.query().convert()

        bindings = sparql_res['results']['bindings']
        if len(bindings) > 0:
            # TODO: handle multi-named directors
            director_name = bindings[0]['director_name']['value']
            return director_name
        else:
            return None

    def _query_writers(self, uri):
        self.endpoint.setQuery(self.query_writer % uri)
        sparql_res = self.endpoint.query().convert()

        bindings = sparql_res['results']['bindings']
        writers = []
        for binding in bindings:
            writer_uri = binding['writer']['value']
            writer_name = self._query_writer_name(writer_uri)
            if writer_name is not None:
                writers.append(writer_name)
        return writers

    def _query_writer_name(self, uri):
        self.endpoint.setQuery(self.query_writer_name % uri)
        sparql_res = self.endpoint.query().convert()

        bindings = sparql_res['results']['bindings']
        if len(bindings) > 0:
            # TODO handle multiple names of one single writer
            writer_name = bindings[0]['writer_name']['value']
            return writer_name
        else:
            return None

    def _query_actors(self, uri):
        self.endpoint.setQuery(self.query_actor % uri)
        sparql_res = self.endpoint.query().convert()

        bindings = sparql_res['results']['bindings']
        actors = []
        for binding in bindings:
            actor_uri = binding['actor']['value']
            actor_name = self._query_actor_name(actor_uri)
            if actor_name is not None:
                actors.append(actor_name)
        return actors

    def _query_actor_name(self, uri):
        self.endpoint.setQuery(self.query_actor_name % uri)
        sparql_res = self.endpoint.query().convert()

        bindings = sparql_res['results']['bindings']

        if len(bindings) > 0:
            # TODO handle multiple names of one singe actor
            actor_name = bindings[0]['actor_name']['value']
            return actor_name
        else:
            return None

    def _query_genres(self, uri):
        # since there are no genres in lmdb, yet
        return None

    def _query_sameAs(self, uri):
        self.endpoint.setQuery(self.query_sameAs % uri)
        sparql_res = self.endpoint.query().convert()

        bindings = sparql_res['results']['bindings']
        links = []
        for binding in bindings:
            link = binding['sameAs']['value']
            if link.startswith('http://dbpedia.org'):
                links.append({'target': 'dbpedia', 'value': link})
        return links
