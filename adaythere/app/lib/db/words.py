from google.appengine.ext import ndb
from app.lib.components.words import WordCount

class Word (ndb.Model):

    word = ndb.StringProperty ()
    count = ndb.IntegerProperty ()

class Words (ndb.Model):

    words = ndb.StructuredProperty (Word, repeated = True)
    day = ndb.KeyProperty ("Day")
    full_locality = ndb.StringProperty ()


    @classmethod
    def add_words (cls, title, description, key, full_locality):

        s = title + " " + description
        wc = WordCount ()
        data = wc.count (s)

        words = Words ()
        words.words = []
        for each in data:
            word = Word ()
            word.word = each
            word.count = data[each]
            words.words.append (word)

        words.day = key
        words.full_locality = full_locality

        words.put ()


    @classmethod
    def delete_words (cls, key):
        words = cls.query (cls.day == key).get ()
        if words is not None:
            words.key.delete () 

    @classmethod
    def update_words (cls, title, description, key, full_locality):
        cls.delete_words (key)
        cls.add_words (title, description, key, full_locality)

    @classmethod
    def query_words (cls, words, full_locality):
        query = cls.query ()
        query = query.filter (cls.full_locality == full_locality)
        for each in words:
            query = query.filter (cls.words.word == each)

        return query


    @classmethod
    def query_days_words (cls, days, words):
        return cls.query (cls.day.IN (days), cls.words.word.IN (words))


