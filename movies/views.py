import sys

from bottle import static_file, request, route, TEMPLATE_PATH, jinja2_template as template
from movies.utils.freebase import FreebaseWrapper

TEMPLATE_PATH.append("./movies/templates")

# setup mongodb (connect to wcm12 database)
from pymongo import Connection
connection = Connection('localhost', 27017)
db = connection.wcm12

@route('/media/:path#.+#', name='static')
def static(path):
    """
    Method for serving static files like stylesheets or images.
    """
    return static_file(path, root='media')

@route('/')
def index():
    """
    This methods provides the main page which shows the movie collection of the
    user or the results of a search.
    """
    if "search" in request.params:
        # TODO query generic mediator
        freebase = FreebaseWrapper()
        films = freebase.get_film_by_name(request.params["search"])
        return films
    else:
        if request.headers['accept'] == "application/json":
            # TODO get user movies
            freebase = FreebaseWrapper()
            films = freebase.get_film_by_name("The Matrix")
            return films
        else:
            return template("index.html")

@route('/:id', method="GET")
def get_movie(id):
    """
    This method delivers all the details available for a given movie.
    """
    if request.headers['accept'] == "application/json":
        # TODO query local db data
        freebase = FreebaseWrapper()
        films = freebase.get_film_by_name(id)
        return films
    else:
        return template("details.html")

@route('/:id', method="PUT")
def put_movie(id):
    """
    This method stores a new movie in the database.
    """
    pass

@route('/:id', method="DELETE")
def delete_movie(id):
    """
    This method deletes a given movie either from the users movie collection or
    completely from the database if no other user owns this movie.
    """
    pass
