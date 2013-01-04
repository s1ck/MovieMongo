# -*- coding: utf-8 -*-
import sys
import re
import json

from bottle import static_file, redirect, request, route, TEMPLATE_PATH, jinja2_template as template
from movies.mediator import Mediator
from movies.wrappers.freebase import FreebaseWrapper
from movies.wrappers.mongodb import MongoDBWrapper
from movies.wrappers.imdbwrapper import IMDBWrapper
from utils import MongoManager
from utils.cork import Cork
from utils.cork.mongo_backend import MongoDbBackend
from movies import settings

TEMPLATE_PATH.append("./movies/templates")

backend = MongoDbBackend(
   server = settings.MONGO_HOST,
   port = settings.MONGO_PORT,
   database = settings.MONGO_DB,
   initialize=False,
   users_store="users",
   roles_store="roles",
   pending_regs_store="register",
)
aaa = Cork(backend)

mongo_mgr = MongoManager(settings.MONGO_HOST, settings.MONGO_PORT)
mediator = Mediator(mongo_mgr)
mediator.add_wrapper(MongoDBWrapper(mongo_mgr))
mediator.add_wrapper(FreebaseWrapper())
mediator.add_wrapper(IMDBWrapper())


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
        return mediator.get_films_by_name(search)
    else:
        if request.headers['accept'] == "application/json":
            # TODO get user movies
            return mediator.get_films_by_name('Matrix')
        else:
            return template("index.html", user=aaa.current_user.username)

@route('/:source', method="GET")
def get_movie(source):
    """
    This method delivers all the details available for a given movie.
    """
    id = request.params.get('id')
    if id and request.headers['accept'] == "application/json":
        films = mediator.get_film_by_id(id, source)
        return films
    else:
        return template("details.html", user=aaa.current_user.username)

@route('/:source', method="POST")
def post_movie(source):
    """
    This method stores a new movie in the database.
    """
    #TODO call mongo manager
    pass

@route('/:source', method="DELETE")
def delete_movie(source):
    """
    This method deletes a given movie either from the users movie collection or
    completely from the database if no other user owns this movie.
    """
    #TODO call mongo manager
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
