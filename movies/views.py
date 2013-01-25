# -*- coding: utf-8 -*-
import sys
import re
import json

from bottle import static_file, redirect, request, route, TEMPLATE_PATH, jinja2_template as template
from bson.json_util import dumps
from movies.mediator import Mediator
from movies.wrappers.freebase import FreebaseWrapper
from movies.wrappers.mongodb import MongoDBWrapper
from movies.wrappers.imdbwrapper import IMDBWrapper
from movies.wrappers.lmdbwrapper import LMDBWrapper
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
   users_store="user",
   roles_store="roles",
   pending_regs_store="register",
)
aaa = Cork(backend)

mongo_mgr = MongoManager(settings.MONGO_HOST, settings.MONGO_PORT)
mediator = Mediator(mongo_mgr)
mediator.add_wrapper(MongoDBWrapper(mongo_mgr))
mediator.add_wrapper(FreebaseWrapper())
#mediator.add_wrapper(IMDBWrapper())
#mediator.add_wrapper(LMDBWrapper())


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

        # split search string and check for special keywords
        keyword = search.split(":")[0]
        arg = ":".join(search.split(":")[1:])
        if keyword in ["actor","director","year"]:
            user_films = mongo_mgr.get_films_by_user(aaa.current_user.id)
            user_films = [film for film in user_films if film is not None]
            user_film_ids = [film["_id"] for film in user_films]

            query = {"_id": {"$in": user_film_ids}}
            if keyword == "actor":
                query["actors"] = {"$in": [arg]}
            elif keyword == "director":
                query["directed_by"] = {"$in": [arg]}
            elif keyword == "year":
                query["initial_release_date"] = int(arg)

            cursor = mongo_mgr.get_films_by_pattern(query)

            films = {"result": cursor}
            films = json.loads(dumps(films))
        else:
            films = mediator.get_films_by_name(search)

        for film in films['result']:
            film['my_movie'] = mongo_mgr.user_has_movie(film['_id']['$oid'], aaa.current_user.id)

        return json.dumps(films)
    else:
        if request.headers['accept'] == "application/json":
            films = mongo_mgr.get_films_by_user(aaa.current_user.id)
            films = [film for film in films if film is not None]
            for film in films:
                film['my_movie'] = True
            return dumps(films)
        else:
            return template("index.html", user=aaa.current_user.username)

@route('/:id', method="GET")
def get_movie(id):
    """
    This method delivers all the details available for a given movie.
    """
    if id and request.headers['accept'] == "application/json":
        film = json.loads(dumps(mongo_mgr.get_film_by_id(id)))
        user_has_movie = mongo_mgr.user_has_movie(id, aaa.current_user.id)
        film['my_movie'] = user_has_movie
        return film
    else:
        return template("details.html", user=aaa.current_user.username)

@route('/', method="POST")
def post_movie():
    """
    This method stores a new movie in the database.
    """
    id = request.params.get('id')
    mongo_mgr.add_film_to_user(id, aaa.current_user.id)

@route('/', method="DELETE")
def delete_movie():
    """
    This method deletes a given movie either from the users movie collection or
    completely from the database if no other user owns this movie.
    """
    id = request.params.get('id')
    mongo_mgr.remove_film_from_user(id, aaa.current_user.id)

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
