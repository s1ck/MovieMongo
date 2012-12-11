# -*- coding: utf-8 -*-


class BaseWrapper(object):
    """Base wrapper class defining the methods to be implemented by all
    other wrappers
    """

    def get_films_by_name(self, name):
        """Returns all films which match the given name.
        Function returns an dictionary, access the films via:
            return_val['result']
        """
        raise NotImplementedError

    def get_name(self):
        """Returns the unique name of the wrapper"""
        raise NotImplementedError

    def get_film_by_id(self, film_id):
        raise NotImplementedError
