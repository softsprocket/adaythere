
from google.appengine.api import users
import webapp2
from app.adaythere import ADayThere
from app.lib.db.keywords import Keywords

class KeywordHandler (webapp2.RequestHandler):

    def get (self):

        tool_user, db_user = ADayThere.tool_user ()
        if not tool_user:
            self.response.status = 401
            return

        keywords = Keywords.query ().fetch ()

        self.response.write (json.dumps (keywords))

