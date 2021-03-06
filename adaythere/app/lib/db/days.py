"""
    ndb days models
"""

from google.appengine.ext import ndb
from app.lib.db.location import Location
import random
from app.lib.db.keywords import Keywords 
from app.lib.db.words import Words
import itertools
import hashlib

class Place (ndb.Model):
    location = ndb.StructuredProperty (Location)
    name = ndb.StringProperty ()
    comment = ndb.StringProperty ()

class DayPhoto (ndb.Model):
    title = ndb.StringProperty ()
    description = ndb.StringProperty ()

class Day (ndb.Model):
    userid = ndb.StringProperty ()
    name = ndb.StringProperty ()
    full_locality = ndb.StringProperty ()
    title = ndb.StringProperty ()
    keywords = ndb.StringProperty (repeated=True)
    description = ndb.StringProperty ()
    places = ndb.StructuredProperty (Place, repeated=True)
    photos = ndb.StructuredProperty (DayPhoto, repeated=True)
    numberOfReviews = ndb.IntegerProperty (default=0)
    averageReview = ndb.IntegerProperty (default=0)

    @classmethod
    def query_user (cls, userid):
        return cls.query (cls.userid == userid)


    @classmethod
    def query_user_title (cls, userid, title):
        return cls.query (cls.userid == userid, cls.title == title)

    @classmethod
    def query_random (cls, num_samples):
        keys = cls.query ().fetch (keys_only=True)

        if (len (keys) < num_samples):
            num_samples = len (keys)

        rv = []
        selected_keys = random.sample (keys, num_samples)
        
        for key in selected_keys:
            rv.append (key.get ())

        return rv

    @classmethod
    def query_days (cls, args):

        cursor = args.get ('cursor', None)
        full_locality = args.get ('full_locality', None)
        minimum_rating = args.get ('minimum_rating', None)
        user_id = args.get ('user_id', None)
        limit = args.get ('limit', 20)

        if cursor is None and full_locality is None:
            return ([], None, False)

        res = (None, None, False)
        filters = []
        
        query = cls.query ()
        if full_locality is not None:
            query = query.filter (cls.full_locality == full_locality)
        if minimum_rating is not None and int(minimum_rating) != 0:
            query = query.filter (cls.averageReview >= minimum_rating)
        if user_id is not None:
            query = query.filter (cls.user_id == user_id)

        if cursor is not None:
            res = query.fetch_page (limit, start_cursor = cursor)
        else:
            res = query.fetch_page (limit)

        return res

    @classmethod
    def query_word_days (cls, args, words):

        cursor = args.get ('cursor', None)
        full_locality = args.get ('full_locality', None)

        if cursor is None and full_locality is None:
            return ([], None, False)

        minimum_rating = args.get ('minimum_rating', None)
        user_id = args.get ('user_id', None)
        limit = args.get ('limit', None)
        all_words = args.get ('all_words', None)

        query_iter = None
        if cursor is not None:
            query_iter = Words.query ().iter (produce_cursors=True, start_cursor=cursor)
        else:
            query = Words.query_words (words, full_locality)
            query_iter = query.iter (produce_cursors=True)
            
            if all_words == 'false':
                pos = 1
                order = 0

                while query_iter is None or query_iter.has_next () is False:
                    if len (words[pos:]) > 1:

                        if order == 0:
                            query = Words.query_words (words[pos:], full_locality)
                            query_iter = query.iter (produce_cursors=True)
                        elif order == 1:
                            query = Words.query_words (words[:len (words) - pos], full_locality)
                            query_iter = query.iter (produce_cursors=True)
                        elif len (words[pos:len (words) - pos]) > 1:
                            query = Words.query_words (words[pos:len(words) - pos], full_locality)
                            query_iter = query.iter (produce_cursors=True)
                        pos += 1
                        if order == 2:
                            order = 0
                        else:
                            order += 1
                    else:
                        for each in words:
                            query = Words.query_words ([each], full_locality)
                            query_iter = query.iter (produce_cursors=True)
                            if query_iter is not None and query_iter.has_next (): 
                                break

                        break


        added = 0
        days = []

        for words in query_iter:
            day = words.day.get ()
            
            if added > 0 and days[added - 1].key == day.key:
                continue

            if user_id is not None and day.user_id != user_id:
                continue

            if minimum_rating is not None and day.averageReview < minimum_rating:
                continue
            
            days.append (day)
            added += 1
            
            if added == limit:
                break

        if query_iter.has_next ():
            cursor = query_iter.cursor_after ()
            more = True
        else:
            cursor = None
            more = False

        return (days, cursor, more)


    @classmethod
    def query_keyword_days (cls, keyhash, args, words):

        full_locality = args.get ('full_locality', None)
        minimum_rating = args.get ('minimum_rating', None)
        user_id = args.get ('user_id', None)
        cursor = args.get ('cursor', None)
        limit = args.get ('limit', None)
        
        if cursor is None and full_locality is None:
            return ([], None, False)

        kdl_query_iter = None
        if cursor is not None:
            kdl_query_iter = KeywordsDayList.query ().iter (produce_cursors=True, start_cursor=cursor)
        else:
            kdl_query = KeywordsDayList.query_keyhash (keyhash, full_locality)
            kdl_query_iter = kdl_query.iter (produce_cursors=True)

        added = 0
        days = []
        for keywords in kdl_query_iter:
            
            for key in keywords.days:
                found_day = key.get ()

                if words is not None:
                    if Words.query_days_words ([found_day.key], words).get () is None:
                        continue

                if user_id is not None and found_day.user_id != user_id:
                    continue

                if minimum_rating is not None and minimum_rating != 0 and found_day.averageReview < minimum_rating:
                    continue

                days.append (found_day)
                added += 1

                if added == limit:
                    break

        if kdl_query_iter.has_next ():
            cursor = kdl_query_iter.cursor_after ()
            more = True
        else:
            cursor = None
            more = False

        return (days, cursor, more)




class KeywordsDayList (ndb.Model):

    keyhash = ndb.StringProperty ()
    days = ndb.KeyProperty (kind=Day, repeated=True)
    full_locality = ndb.StringProperty ()

    @classmethod
    def query_keyhash (cls, keyhash, full_locality):
        return cls.query (cls.keyhash == keyhash, cls.full_locality == full_locality)

    @classmethod
    def add_keywords (cls, day):

        stripped_list = map (lambda x: x.strip (), day.keywords)

        list_len = len (stripped_list)

        for i in range (0, list_len):
            comb = itertools.combinations (stripped_list, i + 1)
            for ea in comb:
                word_list = sorted (map (lambda x: x.strip (), ea))
                keyhash = hashlib.sha256(str(word_list)).hexdigest()
                kq = KeywordsDayList ().query_keyhash (keyhash, day.full_locality)
                kdl = kq.get ()

                if kdl is None:
                    daylist = KeywordsDayList () 
                    daylist.keyhash = keyhash
                    daylist.full_locality = day.full_locality

                    daylist.days = []
                    daylist.days.append (day.key)
                    daylist.put ()
                else:
                    kdl.days.append (day.key)
                    kdl.put ()

            
    @classmethod
    def delete_keywords (cls, day):

        stripped_list = map (lambda x: x.strip (), day.keywords)

        list_len = len (stripped_list)

        for i in range (0, list_len):
            comb = itertools.combinations (stripped_list, i + 1)
            for ea in comb:
                word_list = sorted (map (lambda x: x.strip (), ea))
                keyhash = hashlib.sha256(str(word_list)).hexdigest()
                
                kq = KeywordsDayList ().query_keyhash (keyhash, day.full_locality)
                kdl = kq.get ()

                if kdl is not None:
                    if day.key in kdl.days:
                        kdl.days.remove (day.key)
                        kdl.put ()



