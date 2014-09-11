
"""
    Request handler for /places
"""

import webapp2
import logging
from google.appengine.api import users
import json
from urlparse import urlparse

class LoginHandler (webapp2.RequestHandler):

    def get (self):
        """
            Responds to a get request.
        """

        loginMethod = self.request.get ('method')
   

        data = {}
        if loginMethod == "google":
            data["url"] = users.create_login_url ()
            self.response.write (json.dumps (data))
        else:
            data["url"] = "/"
            self.response.write (json.dumps (data)) 



class LogoutHandler (webapp2.RequestHandler):

    def get (self):
        """
            Responds to a get request.
        """

        loginMethod = self.request.get ('method') 

        data = {}
        if loginMethod == "google":
            data["url"] = users.create_logout_url ("/")
            self.response.write (json.dumps (data))
        else:
            data["url"] = "/"
            self.response.write (json.dumps (data)) 


        
