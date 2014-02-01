"""
    ndb user query model.
"""

from google.appengine.ext import ndb
from app.lib.db.location import Location
import logging
import datetime

class User(ndb.Model):
    user_id = ndb.StringProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    auth_domain = ndb.StringProperty()
    location = ndb.StructuredProperty(Location)
    contributed_adaythere_ids = ndb.IntegerProperty(repeated=True)
    date_joined = ndb.DateTimeProperty()

    @classmethod
    def query_name(cls, name):
        return cls.query(cls.name == name).get()

    @classmethod
    def query_user_id(cls, user_id):
        logging.info("getting " + user_id)
        return cls.query(cls.user_id == user_id).get()

    @classmethod
    def query_email(cls, email):
        cls.email = email
        return cls.query(cls.email == email).get()


    @classmethod
    def create_user_record_from_google_user(cls, google_user):

        stored_user = cls.query_user_id(str(google_user.user_id()))

        if stored_user is None:
            stored_user = User()
            stored_user.user_id = str(google_user.user_id())
            stored_user.email = google_user.email()
            stored_user.name = google_user.nickname()
            stored_user.auth_domain = google_user.auth_domain()
             
            stored_user.date_joined = datetime.datetime.utcnow()
            
            logging.info("putting " + stored_user.user_id)
            stored_user.put()

        return stored_user

