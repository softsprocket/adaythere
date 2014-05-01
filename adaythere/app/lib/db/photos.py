
from google.appengine.ext import ndb


class Photos(ndb.Model):
    user_id = ndb.StringProperty()
    day_title = ndb.StringProperty()
    photo_title = ndb.StringProperty()
    photo = ndb.BlobProperty()
    
    @classmethod
    def query_user_id(cls, user_id):
        return cls.query(cls.user_id == user_id).get()

    @classmethod
    def query_day(cls, user_id, day_title):
        return cls.query(cls.user_id == user_id, cls.day_title == day_title)

    @classmethod
    def query_photo(cls, user_id, day_title, photo_title):
        return cls.query(cls.user_id == user_id, cls.day_title == day_title, cls.photo_title == photo_title)


