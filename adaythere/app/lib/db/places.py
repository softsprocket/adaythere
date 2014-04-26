"""
    ndb places models
"""

from google.appengine.ext import ndb

class Location(ndb.Model):
    latitude = ndb.StringProperty()
    longitude = ndb.StringProperty()

class Place(ndb.Model):
    location = ndb.StructuredProperty(Location)
    name = ndb.StringProperty()
    vicinity = ndb.StringProperty()
    comment = ndb.StringProperty()
    
class Day(ndb.Model):
    userid = ndb.StringProperty()
    locality = ndb.StringProperty()
    title = ndb.StringProperty()
    keywords = ndb.StringProperty(repeated=True)
    description = ndb.StringProperty()
    places = ndb.StructuredProperty(Place, repeated=True)
    numberOfReviews = ndb.IntegerProperty()
    averageReview = ndb.IntegerProperty()

    @classmethod
    def query_user(cls, userid):
        return cls.query(cls.userid == userid)


    @classmethod
    def query_user_title(cls, userid, title):
        return cls.query(cls.userid == userid, cls.title == title)

