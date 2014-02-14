"""
    Request handler for /places
"""

import webapp2
import json
import app.lib.db.user
import logging
from google.appengine.api import users
import inspect
from app.lib.db.location import Location

class ProfileHandler(webapp2.RequestHandler):

    def get(self):
        """
            Responds to a get request.
        """
        user = users.get_current_user()

        if user is None:
            self.response.write("No profile available")
        else:
            logging.info("Profile Getting :" + str(user.user_id()))
            db_user = app.lib.db.user.User.query_user_id(str(user.user_id()))
            logging.info(str(db_user))
            res = self.__build_response(db_user)
            self.response.write(json.dumps(res))


    def post(self):

        user = users.get_current_user()

        db_user = app.lib.db.user.User.query_user_id(str(user.user_id()))

        if db_user is None:
            db_user = app.lib.db.user.User.create_user_record_from_google_user(user)

        location = json.loads(self.request.body)
        logging.info(location)
        db_location = Location()
        db_location.latitude = str(location["location"]["latitude"])
        db_location.longitude = str(location["location"]["longitude"])
        db_location.locality = location["location"]["locality"]
        db_location.address = location["location"]["address"]
        db_user.location = db_location
        db_user.put()
        
        res = self.__build_response(db_user)
        self.response.write(json.dumps(res))


    def __build_response(self, db_user):

        res = {}
        if db_user is not None:
            res["email"] = db_user.email
            res["name"] = db_user.name
            res["auth_domain"] = db_user.auth_domain
            res["user_id"] = db_user.user_id

            res["location"] = {}

            if db_user.location is not None:
                res["location"]["latitude"] = db_user.location.latitude
                res["location"]["longitude"] = db_user.location.longitude
                res["location"]["locality"] = db_user.location.locality
                res["location"]["address"] = db_user.location.address

        return res

