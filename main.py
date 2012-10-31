#!/usr/bin/env python

import sys, os
package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
sys.path.insert(0, package_dir_path)

# open connection to mongodb database wcm12
from pymongo import Connection
connection = Connection('localhost', 27017)
db = connection.wcm12

from bottle import run, route
from movies import views

run(host="localhost", port=8080, debug=True)
