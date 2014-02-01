"""
    ndb models for ratings
"""

from google.appengine.ext import ndb

class Rating(ndb.Model):
    ratedModelId = ndb.StringProperty()
    classification = ndb.IntegerProperty()
    stars = ndb.IntegerProperty()

class AdaythereRating(ndb.Model):
    rating = ndb.StructuredProperty(Rating)
    rid = ndb.StringProperty()

    @classmethod
    def query_id(cls, rid):
        cls.rid = rid
        return cls.query().get()


class PlaceRating(ndb.Model):
    rating = ndb.StructuredProperty(Rating)
    rid = ndb.StringProperty()

    @classmethod
    def query_id(cls, rid):
        cls.rid = rid
        return cls.query().get()


class UserRatingsList(ndb.Model):
    userId = ndb.StringProperty()
    adaythereRatings = ndb.IntegerProperty(repeated=True)
    placeRatings = ndb.IntegerProperty(repeated=True)

    @classmethod
    def query_id(cls, userID):
        cls.userId = userId
        return cls.query().get()

