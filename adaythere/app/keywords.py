
from google.appengine.api import users
import webapp2
from app.adaythere import ADayThere
from app.lib.db.keywords import Keywords
import json

class KeywordHandler (webapp2.RequestHandler):

    def get (self):

        keywords = Keywords.query ().fetch ()

        rv = []
        for keyword in keywords:
            rv.append (keyword.keyword)

        self.response.write (json.dumps (rv))

