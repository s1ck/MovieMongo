#!/usr/bin/env python

import sys, os
package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
sys.path.insert(0, package_dir_path)

from bottle import run, route
from movies import views

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "usage: main.py <google_api_key>"
        sys.exit(1)

    # run the webserver
    run(host="localhost", port=8080, debug=True)
