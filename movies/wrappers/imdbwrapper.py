# -*- coding: utf-8 -*-

from imdb import IMDb

from movies.wrappers.base import BaseWrapper


class IMDBWrapper(BaseWrapper):

    def __init__(self):
        self.name = 'imdb'
        self.__db = IMDb()

    def get_name(self):
        return self.name

    def get_films_by_name(self, name, exclude_ids=[]):
        results = self.__db.search_movie(name)
        # results looks sth like this:
        # >>> pp(results)
        # [<Movie id:0079470[http] title:_Brian di Nazareth (1979)_>,
        #  <Movie id:0654954[http] title:_"My So-Called Life" Life of Brian (1994)_>,
        #  <Movie id:0337896[http] title:_The Life of Brian (2002)_>,
        #  <Movie id:0934946[http] title:_The Secret Life of Brian (2007) (TV)_>,
        #  <Movie id:0107047[http] title:_Atto indecente (1993) (TV)_>,
        #  <Movie id:2229502[http] title:_"World in Action" The Life of Brian (1993)_>,
        #  ...
        movies = []
        for result in results:
            movie_id = result.movieID
            if result['kind'] not in ['movie', 'tv movie'] or \
                    'tt' + movie_id in exclude_ids:
                continue

            # this will take a long long time to finish
            movie = self.__db.get_movie(movie_id)

            movies.append(movie)
        return self._normalize(movies)

    def get_film_by_id(self, film_id):
        film = self.__db.get_movie(film_id[2:])
        return self._normalize([film])

    def _normalize(self, results):
        # source key: (normalized key, transformation method or function
        # to call)
        mappings = {
            'title': ('name', None),
            'year': ('initial_release_date', None),
            'director': ('directed_by', self._resolve_person_names),
            'writer': ('written_by', self._resolve_person_names),
            'cast': ('actors', self._resolve_person_names),
            'genres': ('genre', None),
        }
        mapping_keys = mappings.keys()
        normalized_results = []

        for result in results:
            normalized_res = {}
            for key in result.keys():
                if key in mapping_keys:
                    val = result[key]
                    if mappings[key][1] is not None:
                        method = mappings[key][1]
                        val = method(val)
                    normalized_key = mappings[key][0]
                    normalized_res[normalized_key] = val
            ## add additional information
            # source
            normalized_res['source'] = self.name
            # id
            normalized_res['source_id'] = 'tt' + result.getID()
            # image url
            if result.get('cover url') is not None:
                normalized_res['img_url'] = result['cover url']
            elif result.get('full-size cover url') is not None:
                normalized_res['img_url'] = result['full-size cover url']

            normalized_results.append(normalized_res)
        return {'result': normalized_results}

    def _resolve_person_names(self, persons):
        """:param persons: a list of imdb.Person.Person instances, e.g.:
        [<Person id:0905152[http] name:_Wachowski, Andy_>,
         <Person id:0905154[http] name:_Wachowski, Lana_>]
        """
        names = []
        for person in persons:
            names.append(person['name'])
        return names
