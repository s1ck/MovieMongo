# -*- coding: utf-8 -*-


class BaseWrapper(object):
    """Base wrapper class defining the methods to be implemented by all
    other wrappers
    """

    def get_films_by_name(self, name):
        raise NotImplementedError

    def get_film_by_id(self, film_id):
        raise NotImplementedError
