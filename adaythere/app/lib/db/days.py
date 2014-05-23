"""
    ndb days models
"""

from google.appengine.ext import ndb
from app.lib.db.location import Location
import random
from app.lib.db.keywords import Keywords 

class Place (ndb.Model):
    location = ndb.StructuredProperty (Location)
    name = ndb.StringProperty ()
    comment = ndb.StringProperty ()

class DayPhoto (ndb.Model):
    title = ndb.StringProperty ()
    description = ndb.StringProperty ()

class Day (ndb.Model):
    userid = ndb.StringProperty ()
    locality = ndb.StringProperty ()
    title = ndb.StringProperty ()
    keywords = ndb.StringProperty (repeated=True)
    description = ndb.StringProperty ()
    places = ndb.StructuredProperty (Place, repeated=True)
    photos = ndb.StructuredProperty (DayPhoto, repeated=True)
    numberOfReviews = ndb.IntegerProperty ()
    averageReview = ndb.IntegerProperty ()

    @classmethod
    def query_user (cls, userid):
        return cls.query (cls.userid == userid)


    @classmethod
    def query_user_title (cls, userid, title):
        return cls.query (cls.userid == userid, cls.title == title)

    @classmethod
    def query_random (cls, num_samples, **kwargs):
        keys = None
        
        locality = kwargs.get ('locality')
        minimum_rating = kwargs.get ('minimum_rating')

        if locality is not None and minimum_rating is not None:
            keys = cls.query (cls.locality == locality, averageReview >= minimum_rating).fetch (keys_only=True)
        elif locality is not None:
            keys = cls.query (cls.locality == locality).fetch (keys_only=True)
        elif minimum_rating is not None:
            keys = cls.query (cls.averageReview >= minimum_rating).fetch (keys_only=True)
        else:
            keys = cls.query ().fetch (keys_only=True)

        if (len (keys) < num_samples):
            num_samples = len (keys)

        rv = []
        selected_keys = random.sample (keys, num_samples)
        
        for key in selected_keys:
            rv.append (key.get ())

        return rv

    @classmethod
    def query_days (cls, **kwargs):

        locality = kwargs.get ('locality')
        minimum_rating = kwargs.get ('minimum_rating')
        user_id = kwargs.get ('user_id')
        cursor = kwargs.get ('cursor')
        limit = kwargs.get ('limit')

        if limit is None:
            limit = 20

        filters = []

        if locality is not None:
            filters.append (cls.locality == locality)
        if minimum_rating is not None:
            filters.append (cls.averageReview >= minimum_rating)
        if user_id is not None:
            filters.append (cls.user_id == user_id)
        
        query = cls.query (filters)

        res = None

        if cursor is not None:
            res = query.fetch_page (limit, start_cursor = cursor)
        else:
            res = query.fetch_page (limit)

        return res  

            
    @classmethod
    def query_keyword_days (cls, keyhash, **kwargs):

        locality = kwargs.get ('locality')
        minimum_rating = kwargs.get ('minimum_rating')
        user_id = kwargs.get ('user_id')
        cursor = kwargs.get ('cursor')
        limit = kwargs.get ('limit')
        
        if locality is None:
            return None

        kdl_query = KeywordsDayList.query_keyhash (keyhash, locality)

        kdl_query_iter = kdl_query.iter (produce_cursors=True, start_cursor=cursor)
        for key in kdl_query_iter:
            day = key.get ()





class KeywordsDayList (ndb.Model):

    keyhash = ndb.IntegerProperty ()
    days = ndb.KeyProperty (kind=Day, repeated=True)
    locality = ndb.StringProperty ()

    @classmethod
    def query_keyhash (cls, keyhash, locality):
        return cls.query (cls.keyhash == keyhash, cls.locality == locality)

    @classmethod
    def add_keywords (cls, day):

        a=list (day.keywords)
        b=list (day.keywords)
        b.pop (0)

        keys_tuple = (a, b)

        from_front = True
        for keywords in keys_tuple:
            while keywords:
                keyhash = hash (str (sorted (keywords)))
                kq = KeywordsDayList ().query_keyhash (keyhash, day.locality)
                kdl = kq.get ()

                if kdl is None:
                    daylist = KeywordsDayList () 
                    daylist.keyhash = keyhash
                    daylist.locality = day.locality

                    daylist.days = []
                    daylist.days.append (day.key)
                    daylist.put ()
                else:
                    kdl.days.append (day.key)
                    kdl.put ()

                    if from_front:
                        keywords.pop (0)
                    else:
                        keywords.pop ()

            from_front = False
            
    @classmethod
    def delete_keywords (cls, day):

        a=list (day.keywords)
        b=list (day.keywords)
        b.pop (0)

        keys_tuple = (a, b)

        from_front = True
        for keywords in keys_tuple:
            while keywords:
                keyhash = hash (str (sorted (keywords)))
                kq = KeywordsDayList ().query_keyhash (keyhash, day.locality)
                kdl = kq.get ()

                if kdl is not None:
                    if day.key in kdl.days:
                        kdl.days.remove (day.key)
                        kdl.put ()

                if from_front:
                    keywords.pop (0)
                else:
                    keywords.pop ()

            from_front = False


