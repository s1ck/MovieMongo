import sys
import re
import json

from bottle import static_file, redirect, request, route, TEMPLATE_PATH, jinja2_template as template
from movies.utils.freebase import FreebaseWrapper
from movies.wrappers.mongodb import MongoDBWrapper
from utils.cork import Cork
from utils.cork.mongo_backend import MongoDbBackend

TEMPLATE_PATH.append("./movies/templates")

# setup mongodb (connect to wcm12 database)
from pymongo import Connection
connection = Connection('localhost', 27017)
db = connection.wcm12

backend = MongoDbBackend(
   server = "localhost",
   port = 27017,
   database = "wcm12",
   initialize=False,
   users_store="users",
   roles_store="roles",
   pending_regs_store="register",
)
aaa = Cork(backend)

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
    aaa.require(fail_redirect='/login')

    if "search" in request.params:
        search = request.params['search']

        # TODO the following has to be done by the mediator
        # search mongo first
        mongo = MongoDBWrapper('localhost', 27017)
        films = mongo.get_films_by_name(search)

        # search the APIs
        # freebase
        freebase = FreebaseWrapper()
        films['result'] += freebase.get_film_by_name(search)['result']
        # TODO query generic mediator
        return films
    else:
        if request.headers['accept'] == "application/json":
            # TODO get user movies
            freebase = FreebaseWrapper()
            films = freebase.get_film_by_name("The Matrix")
            return films
        else:
            return template("index.html", user=aaa.current_user.username)

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
        return template("details.html", user=aaa.current_user.username)

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

@route('/register', method='GET')
def register():
    return template("register.html")

@route('/register', method='POST')
def register():
    """Users can create new accounts, but only with 'user' role"""
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    #email_addr = request.POST.get('email_addr', '')
    aaa.register(username, password, "none@example.com")
    redirect("/")

@route('/login', method="GET")
def login_get():
    return template("login.html")

@route('/login', method="POST")
def login():
    """Authenticate users"""
    username = request.params['username'].strip()
    password = request.params['password'].strip()
    aaa.login(username, password, success_redirect='/', fail_redirect='/login')

@route('/logout')
def logout():
    aaa.logout()
