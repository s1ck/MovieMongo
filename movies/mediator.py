# -*- coding: utf-8 -*-

class Mediator(object):
    def __init__(self):
        self._wrappers = {}

    def add_wrapper(self, wrapper):
        self._wrappers[wrapper.get_name()] = wrapper

    def get_films_by_name(self, name):
        films = {}
        films['result'] = []

        for wrapper in self._wrappers.values():
            films['result'] += wrapper.get_films_by_name(name)['result']

        return films

    def get_film_by_id(self, film_id, source):
        if source in wrappers:
            return wrappers[source].get_film_by_id(film_id)
        return None





