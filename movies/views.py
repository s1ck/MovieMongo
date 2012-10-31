import sys

from bottle import static_file, route, TEMPLATE_PATH, jinja2_template as template

TEMPLATE_PATH.append("./movies/templates")

# setup mongodb (connect to wcm12 database)
from pymongo import Connection
connection = Connection('localhost', 27017)
db = connection.wcm12

# connect to freebase using google api key
from movies.utils.freebase import FreebaseWrapper
freebase = FreebaseWrapper(sys.argv[1])

# @route('/media/<filename>')
# def server_static(filename):
#     return static_file(filename, root='media')
@route('/media/:path#.+#', name='static')
def static(path):
    return static_file(path, root='media')

@route('/')
def index():
    return template("index.html")

@route('/film/<film_name>')
def get_film(film_name):
    films = freebase.get_film_by_name(film_name)
    return films
