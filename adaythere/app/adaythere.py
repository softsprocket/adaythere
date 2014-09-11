"""
    Top level class for the website. It generates the main page for adaythere.com
"""
from app.lib.components.document import Html5Document
from app.lib.db.user import User
from google.appengine.api import users
import re

class ADayThere(Html5Document):

    def __init__(self):
        """
            Constructor. Initializes html document.
        """
        
        Html5Document.__init__(self, "A Day There", {"ng-app":"adaythere"})



    @classmethod
    def tool_user(cls):
        user = users.get_current_user()

        if user is None:
            return False, None

        db_user = User.query_user_id(str(user.user_id()))
        if db_user is None or db_user.banned or not db_user.has_tool_access:
            return False, db_user

        return True, db_user


    @classmethod
    def logged_in_user(cls):
        user = users.get_current_user()
        if user is None:
            return False, None

        db_user = User.query_user_id(str(user.user_id()))

        if db_user is None:
            db_user = User.record_from_google_user (user)
                    
        return True, db_user


    @classmethod
    def admin_user(cls, db_user):
        if re.match (".*@adaythere.com?", db_user.email):
            return True

        return False

