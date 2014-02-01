"""
    ndb places models
"""

from google.appengine.ext import ndb
from app.lib.db.location import Location

class Place(ndb.Model):
    placeId = ndb.StringProperty()
    name = ndb.StringProperty()
    location = ndb.StructuredProperty(Location)
    formattedAddress = ndb.StringProperty()
    classification = ndb.IntegerProperty(repeated=True)
    numberOfReviews = ndb.IntegerProperty()
    averageReview = ndb.IntegerProperty()

    @classmethod
    def query_id(cls, placeId):
        return cls.query(cls.placeId == placeId).get()


class Adaythere(ndb.Model):
    adaythereId = ndb.StringProperty()
    userId = ndb.IntegerProperty()
    rating = ndb.IntegerProperty()
    places = ndb.IntegerProperty(repeated=True)
    description = ndb.TextProperty()

    @classmethod
    def query_id(cls, adaythereId):
        return cls.query(cls.adaythereId == adaythereId).get()


