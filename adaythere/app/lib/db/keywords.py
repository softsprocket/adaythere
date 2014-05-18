
from google.appengine.ext import ndb
from app.lib.db.days import Day

class Keywords(ndb.Model):

    keyword = ndb.StringProperty()

    @classmethod
    def add_if_missing(cls, keyword):
        keywords = cls.query().fetch()

        if keyword in keywords:
            return

        kw = Keywords()
        kw.keyword = keyword
        kw.put()


class KeywordsDayList(ndb.Model):

    keyhash = ndb.IntegerProperty()
    days = ndb.KeyProperty(kind=Day, repeated=True)
    locality = ndb.StringProperty()

    @classmethod
    def query_keyhash(cls, keyhash, locality):
        return cls.query(cls.keyhash == keyhash, cls.locality == locality)

    @classmethod
    def add_keywords(cls, day):

        a=list(day.keywords)
        b=list(day.keywords)
        b.pop(0)

        keys_tuple = (a, b)
        
        from_front = True
        for keywords in keys_tuple:
            while keywords:
                keyhash = hash(str(sorted(keywords)))
                kq = KeywordsDayList().query_keyhash(keyhash, day.locality)
                kdl = kq.get()

                if kdl is None:
                    daylist = KeywordsDayList()
                    daylist.keyhash = keyhash
                    daylist.locality = day.locality

                    daylist.days = []
                    daylist.days.append(day.key)
                    daylist.put()
                else:
                    kdl.days.append(day.key)
                    kdl.put()

                if from_front:
                    keywords.pop(0)
                else:
                    keywords.pop()

            from_front = False

    @classmethod
    def delete_keywords(cls, day):

        a=list(day.keywords)
        b=list(day.keywords)
        b.pop(0)

        keys_tuple = (a, b)
        
        from_front = True
        for keywords in keys_tuple:
            while keywords:

                keyhash = hash(str(sorted(keywords)))
                kq = KeywordsDayList().query_keyhash(keyhash, day.locality)
                kdl = kq.get()

                if kdl is not None:
                    if day.key in kdl.days:
                        kdl.days.remove(day.key)
                        kdl.put()

                if from_front:
                    keywords.pop(0)
                else:
                    keywords.pop()

            from_front = False
                
