"""
    Request handler for /places
"""

import webapp2
import json
import app.lib.db.user
import logging
from google.appengine.api import users
import inspect

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
            res = {}
            if db_user is not None:
                res["email"] = db_user.email
                res["name"] = db_user.name
                res["location"] = db_user.location
                res["auth_domain"] = db_user.auth_domain
                res["user_id"] = db_user.user_id

            self.response.write(json.dumps(res))


    def post(self):

        user = users.get_current_user()

        db_user = app.lib.db.user.User.query_user_id(str(user.user_id()))
        db_user.location = self.request.get('location')
        db_user.put()
        
        res["email"] = db_user.email
        res["name"] = db_user.name
        res["location"] = db_user.location
        res["auth_domain"] = db_user.auth_domain
        res["user_id"] = db_user.user_id

        self.response.write(json.dumps(res))

