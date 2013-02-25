#!/usr/bin/env python

import sys
import pymongo

c = pymongo.MongoClient('mongodb://localhost')
db = c.wcm12
roles = db.roles
properties = db.properties

# insert roles
if roles.count () == 0:
    roles.save({'role': 'admin', 'level': 100})
    roles.save({'role': 'editor', 'level': 60})
    roles.save({'role': 'user', 'level': 50})
else:
    print 'roles already exist'

# insert properties

# cache invalidation (1 hour)
if properties.count () == 0:
    properties.save({'_id': 'cache_invalidation_interval', 'value': 3600})
else:
    print 'properties already exist'
