"""
    ndb days models
"""

from google.appengine.ext import ndb
from app.lib.db.location import Location
import random


class Place(ndb.Model):
    location = ndb.StructuredProperty(Location)
    name = ndb.StringProperty()
    comment = ndb.StringProperty()

class DayPhoto(ndb.Model):
    title = ndb.StringProperty()
    description = ndb.StringProperty()

class Day(ndb.Model):
    userid = ndb.StringProperty()
    locality = ndb.StringProperty()
    title = ndb.StringProperty()
    keywords = ndb.StringProperty(repeated=True)
    description = ndb.StringProperty()
    places = ndb.StructuredProperty(Place, repeated=True)
    photos = ndb.StructuredProperty(DayPhoto, repeated=True)
    numberOfReviews = ndb.IntegerProperty()
    averageReview = ndb.IntegerProperty()

    @classmethod
    def query_user(cls, userid):
        return cls.query(cls.userid == userid)


    @classmethod
    def query_user_title(cls, userid, title):
        return cls.query(cls.userid == userid, cls.title == title)

    @classmethod
    def query_random(cls, num_samples, minimum_rating=None):
        keys = None

        if minimum_rating is not None:
            keys = cls.query(averageReview == minimum_rating).fetch(keys_only=True)
        else:
            keys = cls.query().fetch(keys_only=True)

        if (len(keys) < num_samples):
            num_samples = len(keys)

        rv = []
        selected_keys = random.sample(keys, num_samples)
        
        for key in selected_keys:
            rv.append(key.get())

        return rv

