import re
import webapp2
from google.appengine.api import users as api_users
from app.lib.db.user import User
import cgi
from google.appengine.ext import ndb
import json

class ProfilesHandler (webapp2.RequestHandler):
    max_limit = 10

    def get (self):
        
        tool_user, db_user = ADayThere.tool_user ()

        if not tool_user or not ADayThere.admin_user (db_user):
            self.response.status = 401 
            self.response.write ("Unauthorized")
            return

        query = User.query ()
        if 'name' in self.request.GET.keys ():
            name = self.request.GET['name']
            if name != '':
                query = query.filter (User.name == name) 

        if 'email' in self.request.GET.keys ():
            email = self.request.GET['email']
            if email != '':
                query = query.filter (User.email == email)

        if 'uid' in self.request.GET.keys ():    
            uid = self.request.GET['userid']
            if uid != '':
                query = query.filter (User.user_id == uid)


        limit = self.request.get ('limit', None)
        if limit is None:
            limit = ProfilesHandler.max_limit

        cursor = ndb.Cursor (urlsafe=self.request.get ('cursor'))

        users, cursor, more = query.fetch_page (int (limit), start_cursor=cursor)

        users_arr = []

        for each in users:
            u = self.__build_user (each)
            users_arr.append (u)

        safe_cursor = ''
        if cursor:
            safe_cursor = cursor.urlsafe ()

        resp_obj = {
            "users": users_arr,
            "cursor": safe_cursor,
            "more": more
        }

        resp = json.dumps (resp_obj)
        self.response.write (resp)


    def post (self):
        
        tool_user, db_user = ADayThere.tool_user ()

        if not tool_user or not ADayThere.admin_user (db_user):
            self.response.status = 401 
            self.response.write ("Unauthorized")
            return

        user = json.loads (self.request.body)
        record = User.query_user_id (user['user_id'])
        
        if 'type' not in self.request.GET.keys ():
            self.response.status = 400
        else:
            tp = self.request.GET['type']
            if tp == 'ban':
                record.banned = user['banned']
                record.put ()
                self.response.status = 200
            else:
                self.response.status = 400


        

    def __build_user (self, db_user):

        res = {}
        if db_user is not None:
            res["email"] = db_user.email
            res["name"] = db_user.name
            res["auth_domain"] = db_user.auth_domain
            res["user_id"] = db_user.user_id
    
            if db_user.banned:
                res["banned"] = True
            else:
                res["banned"] = False

            res["location"] = {}
            if db_user.location is not None:
                res["location"]["latitude"] = db_user.location.latitude
                res["location"]["longitude"] = db_user.location.longitude
                res["location"]["locality"] = db_user.location.locality
                res["location"]["address"] = db_user.location.address

        return res

    
