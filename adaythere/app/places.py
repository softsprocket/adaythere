"""
    Request handler for /places
"""

import webapp2
import json
from app.lib.db.places import Location, Place, Day
import logging
from google.appengine.api import users
from app.lib.db.user import User

class PlacesHandler(webapp2.RequestHandler):

    def put(self):

        user = users.get_current_user()
        if user is None:
            self.response.status = 401
            return

        db_user = User.record_from_google_user(user)
        if db_user.banned:
            self.response.status = 401

        print(self.request.body)
        data = json.loads(self.request.body)
        print(data)

        day = Day()
        day.userid = db_user.user_id
        day.locality = data['locality']
        day.title = data['title']
        day.description = data['description']

        if ',' in data['keywords']:
            day.keywords = data['keywords'].split(',')
        else:
            day.keywords = data['keywords'].split(' ')

        day.places = []
        for place in data['places']:
            p = Place()
            p.name = place['name']
            p.comment = place['comment']
            p.location = Location()
            p.location.latitude = str(place['location']['latitude'])
            p.location.longitude = str(place['location']['longitude'])
            p.vicinity = place['vicinity']
            day.places.append(p)

        day.put()

        print(day)
        self.response.status = 200

    def get(self):

        user = users.get_current_user()
        if user is None:
            self.response.status = 401
            return
                                                
        db_user = User.record_from_google_user(user)
        if db_user.banned:
            self.response.status = 401

        days = []
        #count = Day.query(Day.userid == db_user.user_id).count()
        data = Day.query_user(db_user.user_id).fetch()
        for each in data:
            days.append(json.dumps(each.to_dict()))
            
        self.response.write(json.dumps(days))



