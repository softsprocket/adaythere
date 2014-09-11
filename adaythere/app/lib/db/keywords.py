
from google.appengine.ext import ndb

class Keywords (ndb.Model):

    keyword = ndb.StringProperty ()

    @classmethod
    def add_if_missing (cls, keyword):
        keyword = keyword.strip ()
        word = cls.query (cls.keyword == keyword ).get ()

        if word is not None:
            return

        kw = Keywords ()
        kw.keyword = keyword
        kw.put ()


