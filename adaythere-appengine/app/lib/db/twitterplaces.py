"""
    ndb twitter places query model.
"""

from google.appengine.ext import ndb

class PlacesQuery(ndb.Model):
    place = ndb.StringProperty()
    content = ndb.JsonProperty()

    @classmethod
    def query_place(cls, place):
        cls.place = place
        return cls.query().get()

