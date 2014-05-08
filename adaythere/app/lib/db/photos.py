
from google.appengine.ext import ndb


class Photos(ndb.Model):
    user_id = ndb.StringProperty()
    title = ndb.StringProperty()
    photo = ndb.BlobProperty()
    used_by = ndb.StringProperty(repeated=True)

    @classmethod
    def query_user_id(cls, user_id):
        return cls.query(cls.user_id == user_id)

    @classmethod
    def query_photo(cls, user_id, photo_title):
        return cls.query(cls.user_id == user_id, cls.title == photo_title)


