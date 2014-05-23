
from google.appengine.ext import ndb

class Keywords (ndb.Model):

    keyword = ndb.StringProperty ()

    @classmethod
    def add_if_missing (cls, keyword):
        keywords = cls.query ().fetch ()

        if keyword in keywords:
            return

        kw = Keywords ()
        kw.keyword = keyword
        kw.put ()


