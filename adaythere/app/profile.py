"""
    Request handler for /places
"""

import webapp2
import json
from app.lib.db.user import User
import logging
import inspect
from app.lib.db.location import Location
import datetime
from app.adaythere import ADayThere

class ProfileHandler (webapp2.RequestHandler):

    def get (self):
        """
            Responds to a get request.
        """

        logged_in, user = ADayThere.logged_in_user ()
        if not logged_in:
            self.response.status = 401
            return

        db_user = User.query_user_id (str (user.user_id ()))
        logging.info (str (db_user))
        res = self.__build_response (db_user)
        self.response.write (json.dumps (res))


    def post (self):

        logged_in, user = ADayThere.logged_in_user ()
        if not logged_in:
            self.response.status = 401
            return
        
        db_user = User.query_user_id (str (user.user_id ()))

        location = json.loads (self.request.body)
        logging.info (location)
        db_location = Location ()
        db_location.latitude = str (location["location"]["latitude"])
        db_location.longitude = str (location["location"]["longitude"])
        db_location.locality = location["location"]["locality"]
        db_location.vicinity = location["location"]["vicinity"]
        db_user.location = db_location
        db_user.put ()
        
        res = self.__build_response (db_user)
        self.response.write (json.dumps (res))



    def put (self):

        logged_in, user = ADayThere.logged_in_user ()
        if not logged_in:
            self.response.status = 401
            return
    
        operation = self.request.get ("operation")

        if operation == 'add_tool_access':
            db_user = User.query_user_id (str (user.user_id ()))
            if db_user is not None and db_user.has_tool_access:
                return

            db_user.has_tool_access = True
            db_user.date_agreed_to_tool_access = datetime.datetime.utcnow ()
            db_user.put ()


    def __build_response (self, db_user):

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
                res["location"]["vicinity"] = db_user.location.vicinity

        return res

