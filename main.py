#!/usr/bin/env python

import sys, os
package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
sys.path.insert(0, package_dir_path)

from bottle import run, route

# run the webserver
run(host="localhost", port=8080, debug=True)
