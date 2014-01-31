"""
    ndb location model
"""
from google.appengine.ext import ndb

class Location(ndb.Model):
    latitude = ndb.StringProperty()
    longitude = ndb.StringProperty()
    locality = ndb.StringProperty()
    address  = ndb.StringProperty()
