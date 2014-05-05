"""
    Request handler for /places
"""

import webapp2
import json
from app.lib.db.places import Location, Place, Day
import logging
from app.lib.db.user import User
from app.adaythere import ADayThere

class PlacesHandler(webapp2.RequestHandler):

    def put(self):

        tool_user, db_user = ADayThere.tool_user()
        if not tool_user:
            self.response.status = 401
            return

        data = json.loads(self.request.body)

        day = Day()
        day.userid = db_user.user_id
        day.locality = data['locality']
        day.title = data['title']
        day.description = data['description']

        if isinstance(data['keywords'], basestring):
            if ',' in data['keywords']:
                day.keywords = data['keywords'].split(',')
            else:
                day.keywords = data['keywords'].split(' ')
        else:
            day.keywords = data['keywords']
        
        day.places = []
        for place in data['places']:
            p = Place()
            p.name = place['name']
            p.comment = place['comment']
            p.location = Location()
            p.location.latitude = str(place['location']['latitude'])
            p.location.longitude = str(place['location']['longitude'])
            p.location.vicinity = place['vicinity']
            day.places.append(p)

        day.put()

        self.response.status = 200

    def get(self):

        tool_user, db_user = ADayThere.tool_user()
        if not tool_user:
            self.response.status = 401
            return

        days = []
        data = Day.query_user(db_user.user_id).fetch()

        print data

        for each in data:
            days.append(json.dumps(each.to_dict()))
            
        self.response.write(json.dumps(days))



    def post(self):

        tool_user, db_user = ADayThere.tool_user()
        if not tool_user:
            self.response.status = 401
            return

        data = json.loads(self.request.body)

        day = Day.query_user_title(db_user.user_id, data['title']).get ()

        day.locality = data['locality']
        day.title = data['title']
        day.description = data['description']

        if isinstance(data['keywords'], basestring):
            if ',' in data['keywords']:
                day.keywords = data['keywords'].split(',')
            else:
                day.keywords = data['keywords'].split(' ')
        else:
            day.keywords = data['keywords']

        day.places = []
        for place in data['places']:
            p = Place()
            p.name = place['name']
            p.comment = place['comment']
            p.location = Location()
            p.location.latitude = str(place['location']['latitude'])
            p.location.longitude = str(place['location']['longitude'])
            p.location.vicinity = place['vicinity']
            day.places.append(p)

        day.put ()

        self.response.status = 200


    def delete(self):

        tool_user, db_user = ADayThere.tool_user()
        if not tool_user:
            self.response.status = 401
            return

        title = self.request.get ('title');
        day = Day.query_user_title(db_user.user_id, title)

        day.get ().key.delete ()

        self.response.status = 200

