import re
import webapp2
from google.appengine.api import users as api_users
from app.lib.db.user import User
from app.lib.db.days import Day
import cgi
from google.appengine.ext import ndb
import json
from app.adaythere import ADayThere

class AdminHandler (webapp2.RequestHandler):

    def get (self):
        tool_user, db_user = ADayThere.tool_user ()

        if not ADayThere.admin_user (db_user):
            self.response.status = 401
            self.response.write ("Unauthorized")
            return

        adaythere = ADayThere ()
        adaythere.add_meta_tags ([
            { "charset":"UTF-8" },
            { "http-equiv":"X-UA-Compatible", "content":"IE=edge" },
            { "name":"viewport", "content":"initial-scale=1"}
        ])

        adaythere.add_links ([
            { "rel":"stylesheet", "href":"css/bootstrap.css" },
            { "rel":"stylesheet", "href":"css/adaythere.css" }
        ])
        
        adaythere.add_script_tags_for_body ([
            { "src":"js/jquery-1.11.0-beta2.js" },
            { "src":"js/angular/angular.min.js" },
            { "src":"js/angular/angular-route.min.js" },
            { "src":"js/ui-bootstrap-tpls-0.10.0.min.js" },
            { "src":"js/adaythere.js" }
        ])

        
        adaythere.open_element ("header", {"id":"page_header"})
        adaythere.open_element ("h1", {"id":"page_heading"}, "A Day There - Administration Page")
        adaythere.close_element ("h1")
        adaythere.open_element ("nav")
        adaythere.append_to_element ("")
        adaythere.close_element ("nav")
        adaythere.close_element ("header")

        adaythere.open_element ("section", {"ng-controller":"adminCtrl", "style":"width:600px;margin:0px auto;"})

        adaythere.open_element ("div", {"id":"admin_profile_div"})

        type = self.request.get ('type', default_value=None)

        if type is not None:
            if type == 'profiles':
                self.get_profile_form (adaythere)
            elif type == 'days':
                self.get_days_form (adaythere)

        adaythere.close_element ("div")

        adaythere.close_element ("section")

        adaythere.open_element ("footer", {"id":"page_footer"})
        adaythere.open_element ("p", None, "&copy; 2014 SoftSprocket")
        adaythere.close_element ("p")
        adaythere.close_element ("footer")

        self.response.status = 200
        self.response.write (adaythere.get ())

    def get_profile_form (self, adaythere):
        adaythere.append_to_element ("""
            <h3>Profiles</h3>
        """)
        adaythere.append_to_element ("""
        <label for="name">Name: </label>
        <input id="name" class="form-control" type='text' ng-model='profile_search_on.name'></input>
        <label for="email">Email: </label>
        <input id="email" class="form-control" type='text' ng-model='profile_search_on.email'></input>        
        <label for="userid">UserId: </label>
        <input id="userid" class="form-control" type='text' ng-model='profile_search_on.userid'></input>
        """)
        adaythere.append_to_element ("""
        <button class="btn btn-primary" ng-click="adminprofile_search ()">Search</button>
        <div>----------------------------------------------------------------</div>
        <div ng-repeat="user in received_profile_data.users">
            <ul>
                <li>
                    <label>User ID</label>
                    <input class="form-control" type="text" ng-model="user.user_id" readonly></input>
                    <label>Email</label>
                    <input class="form-control" type="text" ng-model="user.email"></input>
                    <label>Auth Domain</label>
                    <input class="form-control" type="text" ng-model="user.auth_domain" readonly></input>
                    <label>User Name</label>
                    <div id="admin_name_choice{{ $index }}" style="color:red;"></div>
                    <input data-warning-id="admin_name_choice{{ $index }}" class="form-control" type="text" ng-model="user.name" contributor-user-name></input>
                    <label>Banned</label>
                    <input class="form-control" type="text" ng-model="user.banned" readonly></input>
                    <button ng-click="adminprofile_change_ban (user)">Change Ban</button>

                </li>
            </ul>
            <div id="admin_feedback_div{{ $index }}" style="color:red;"></div>
            <button ng-click="save_changed_user (user, '#admin_feedback_div' + $index)">Save</button>
            <div>----------------------------------------------------------------</div>
        </div>
        <div ng-if="received_profile_data.more">More</div>
        """)

    def get_days_form (self, adaythere):
        adaythere.append_to_element ("""
            <h3>Days</h3>
        """)
        adaythere.append_to_element ("""
        <label for="name">By user name: </label>
        <input id="name" class="form-control" type='text' ng-model='days_search_on.name'></input>
        <label for="title">By title: </label>
        <input id="title" class="form-control" type='text' ng-model='days_search_on.title'></input>        
        <label for="locale">By locale: </label>
        <input id="locale" class="form-control" type='text' ng-model='days_search_on.locale'></input>
        """)
        adaythere.append_to_element ("""
        <button class="btn btn-primary" ng-click="admindays_search ()">Search</button>
        <div>----------------------------------------------------------------</div>
        <div ng-repeat="day in received_days_data.days">
            <ul>
                <li>
                    <label>User Id</label>
                    <input class="form-control" type="text" ng-model="day.userid" readonly></input>
                    <label>Name</label>
                    <input class="form-control" type="text" ng-model="day.name" readonly></input>
                    <label>Title</label>
                    <input class="form-control" type="text" ng-model="day.title" readonly></input>
                    <label>Description</label>
                    <input class="form-control" type="text" ng-model="day.description" readonly></input>
                    <label>Locale</label>
                    <input class="form-control" type="text" ng-model="day.locale" readonly></input>

                    <button ng-click="admindays_delete_day (day)">Delete</button>

                </li>
            </ul>
            <div>----------------------------------------------------------------</div>
        </div>
        <div ng-if="received_profile_data.more">More</div>
        """)

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

        if 'user_id' in self.request.GET.keys ():    
            uid = self.request.GET['user_id']
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

   

class DaysHandler (webapp2.RequestHandler):
    max_limit = 10
    
    def get (self):
        
        tool_user, db_user = ADayThere.tool_user ()

        if not ADayThere.admin_user (db_user):
            self.response.status = 401
            self.response.write ("Unauthorized")
            return

        query = Day.query ()
        if 'name' in self.request.GET.keys ():
            name = self.request.GET['name']
            if name != '':
                query = query.filter (Day.name == name) 

        if 'title' in self.request.GET.keys ():
            title = self.request.GET['title']
            if title != '':
                query = query.filter (Day.title == title)

        if 'locale' in self.request.GET.keys ():    
            locale = self.request.GET['locale']
            if locale != '':
                query = query.filter (Day.full_locality == locale)

        limit = self.request.get ('limit', None)
        if limit is None:
            limit = DaysHandler.max_limit

        cursor = ndb.Cursor (urlsafe=self.request.get ('cursor'))

        days, cursor, more = query.fetch_page (int (limit), start_cursor=cursor)

        days_arr = []

        for each in days:
            d = self.__build_day (each)
            days_arr.append (d)

        safe_cursor = ''
        if cursor:
            safe_cursor = cursor.urlsafe ()

        resp_obj = {
            "days": days_arr,
            "cursor": safe_cursor,
            "more": more
        }

        resp = json.dumps (resp_obj)
        self.response.write (resp)


    def __build_day (self, day):

        res = {}
        if day is not None:
            res["userid"] = day.userid
            res["name"] = day.name
            res["locale"] = day.full_locality
            res["title"] = day.title
            res["description"] = day.description

        return res


    def post (self):
        
        tool_user, db_user = ADayThere.tool_user ()

        if not ADayThere.admin_user (db_user):
            self.response.status = 401 
            self.response.write ("Unauthorized")
            return

        sent_day = json.loads (self.request.body)
    
        day_query = Day.query_user_title (sent_day['userid'], sent_day['title'])
        day = day_query.get ()
        if day is None:
            self.response.status = 404
            self.response.write ("Not Found")
            return

        day.key.delete ()

        self.response.status = 200
        self.response.write ("OK")


