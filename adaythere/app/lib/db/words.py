from google.appengine.ext import ndb
from app.lib.components.words import WordCount

class Word (ndb.Model):

    word = ndb.StringProperty ()
    count = ndb.IntegerProperty ()

class Words (ndb.Model):

    words = ndb.StructuredProperty (Word, repeated = True)
    day = ndb.KeyProperty ("Day")
    locality = ndb.StringProperty ()


    @classmethod
    def add_words (cls, title, description, key, locality):

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
        words.locality = locality

        words.put ()


    @classmethod
    def delete_words (cls, key):
        words = cls.query (cls.day == key).get ()
        words.key.delete () 

    @classmethod
    def update_words (cls, title, description, key, locality):
        cls.delete_words (key)
        cls.add_word (title, description, key, locality)

    @classmethod
    def query_words (cls, words, locality):
        query = cls.query ()
        query = query.filter (cls.locality == locality)
        for each in words:
            query = query.filter (cls.words.word == each)

        return query


    @classmethod
    def query_days_words (cls, days, words):
        return cls.query (cls.day.IN (days), cls.words.word.IN (words))


