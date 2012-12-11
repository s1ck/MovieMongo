#!/usr/bin/env python

import sys, os
package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
sys.path.insert(0, package_dir_path)

from bottle import app, run, route
from movies import views
from beaker.middleware import SessionMiddleware

# Cork uses Beaker for sessions.
# Define how we want our sessions
session_opts = {
   'session.type': 'cookie',
   'session.validate_key': True,
   'session.cookie_expires': True,
   'session.timeout': 3600 * 24, # 1 day
   'session.encrypt_key': 'please use a random key and keep it secret!',
}

# Hook Beaker sessions up to our default Bottle app
app = SessionMiddleware(app(), session_opts)

# run the webserver
run(host="localhost", port=8080, app=app, debug=True)
