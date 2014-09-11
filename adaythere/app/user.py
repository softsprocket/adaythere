
import webapp2
from app.lib.db.user import User
from app.adaythere import ADayThere
import re

class UsersHandler (webapp2.RequestHandler):

    def get (self):

        logged_in, db_user = ADayThere.logged_in_user ()

        if not logged_in:
            self.response.status = 401
            return

        name = self.request.get ('name', None)
        if name is None:
            self.response,status = 400
            self.response.write ("Name required")
            return 

        user = User.query_name (name)

        self.response.status = 200
        if user is not None:
            self.response.write ('not available')
        else:
            self.response.write ('available')


    def post (self):

        logged_in, db_user = ADayThere.logged_in_user ()

        if not logged_in:
            self.response.status = 401
            return

        name = self.request.get ('name', None)
        matched = re.match ("^[a-z0-9_]+$", name, re.IGNORECASE)

        if name is None or matched is None:
            self.response,status = 400
            self.response.write ("Valid name required")
            return

        response = db_user.update_username (name)

        if response == False:
            self.response.status = 409
            self.response.write (' name is in use ')
            return
       
        self.response.status = 200
        self.response.write (name)

        

