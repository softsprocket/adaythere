from uuid import uuid4
from app.lib.db.user import User
import datetime
import logging
import inspect

class UserModel:

    def __init__(self, user):

        if user.user_id() is not None:
            self.stored_user = User.query_user_id(str(user.user_id()))
        elif user.email() is not None:
            self.stored_user = User.query_email(user.email())
        elif user.nickname() is not None:
            self.stored_user = User.query_name(user.nickname())
        else:
            self.stored_user = None
            
        if self.stored_user is None:
            self.__create_user_record(user)

    
    def __create_user_record(self, user):

        self.stored_user = User()

        if user.user_id() is None:
            self.stored_user.user_id = uuid4()
        else:
            self.stored_user.user_id = str(user.user_id())

        if user.email() is not None:
            self.stored_user.email = user.email() 
        
        if user.nickname() is not None:
            self.stored_user.name = user.nickname()

        if user.auth_domain() is not None:
            self.stored_user.auth_domain = user.auth_domain()

        self.stored_user.date_joined = datetime.datetime.utcnow()
     
        logging.info("putting " + self.stored_user.user_id)
        self.stored_user.put()

    def name(self):
        return self.stored_user.name

