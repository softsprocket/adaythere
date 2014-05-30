"""
    Request handler for /days
"""

import webapp2
import json
from app.lib.db.days import Location, Place, Day, DayPhoto
import logging
from app.lib.db.user import User
from app.lib.db.photos import Photos
from app.adaythere import ADayThere
from app.lib.db.keywords import Keywords
from app.lib.db.days import KeywordsDayList

class DayHandler (webapp2.RequestHandler):

    def put (self):

        tool_user, db_user = ADayThere.tool_user ()
        if not tool_user:
            self.response.status = 401
            return

        data = json.loads (self.request.body)

        day = Day ()
        day.userid = db_user.user_id
        day.locality = data['locality']
        day.title = data['title']
        day.description = data['description']

        if isinstance (data['keywords'], basestring):
            if ',' in data['keywords']:
                day.keywords = data['keywords'].split (',')
            else:
                day.keywords = data['keywords'].split (' ')
        else:
            day.keywords = data['keywords']

        for keyword in day.keywords:
            Keywords.add_if_missing (keyword)



        day.places = []
        for place in data['places']:
            p = Place ()
            p.name = place['name']
            p.comment = place['comment']
            p.location = Location ()
            p.location.latitude = str (place['location']['latitude'])
            p.location.longitude = str (place['location']['longitude'])
            p.location.vicinity = place['vicinity']
            day.places.append (p)

        day.photos = []
        for photo in data['photos']:
            day_photo = DayPhoto ()
            day_photo.title = photo['title']
            day_photo.description = photo['description']

            day.photos.append (day_photo)

            photo_query = Photos.query_photo (db_user.user_id, photo['title'])
            pq = photo_query.get ()
            cnt = pq.used_by.count (day.title)
            if (cnt == 0):
                pq.used_by.append (day.title)

            pq.put ()


        day.put ()

        KeywordsDayList.add_keywords (day)

        self.response.status = 200


    def get (self):

        tool_user, db_user = ADayThere.tool_user ()
        if not tool_user:
            self.response.status = 401
            return

        days = []
        data = Day.query_user (db_user.user_id).fetch ()

        print data

        for each in data:
            days.append (json.dumps (each.to_dict ()))

        self.response.write (json.dumps (days))



    def post (self):

        tool_user, db_user = ADayThere.tool_user ()
        if not tool_user:
            self.response.status = 401
            return

        data = json.loads (self.request.body)

        day = Day.query_user_title (db_user.user_id, data['title']).get ()

        KeywordsDayList.delete_keywords (day)
        
        day.locality = data['locality']
        day.title = data['title']
        day.description = data['description']

        if isinstance (data['keywords'], basestring):
            if ',' in data['keywords']:
                day.keywords = data['keywords'].split (',')
            else:
                day.keywords = data['keywords'].split (' ')
        else:
            day.keywords = data['keywords']

        for keyword in day.keywords:
            Keywords.add_if_missing (keyword)

        day.places = []
        for place in data['places']:
            p = Place ()
            p.name = place['name']
            p.comment = place['comment']
            p.location = Location ()
            p.location.latitude = str (place['location']['latitude'])
            p.location.longitude = str (place['location']['longitude'])
            p.location.vicinity = place['vicinity']
            day.places.append (p)

        day.photos = []
        for photo in data['photos']:
            day_photo = DayPhoto ()
            day_photo.title = photo['title']
            day_photo.description = photo['description']

            day.photos.append (day_photo)

            photo_query = Photos.query_photo (db_user.user_id, photo['title'])
            pq = photo_query.get ()
            cnt = pq.used_by.count (day.title)
            if (cnt == 0):
                pq.used_by.append (day.title)

        day.put ()

        KeywordsDayList.add_keywords (day)

        self.response.status = 200


    def delete (self):

        tool_user, db_user = ADayThere.tool_user ()
        if not tool_user:
            self.response.status = 401
            return

        title = self.request.get ('title');
        day = Day.query_user_title (db_user.user_id, title).get ()

        for photo in day.photos:
            photo_query = Photos.query_photo (db_user.user_id, photo.title)
            pq = photo_query.get ()
            try:
                index = pq.index (day.title)
                day.title.pop (index)
            except:
                pass

            pq.key.delete ()


        day.key.delete ()
        
        KeywordsDayList.delete_keywords (day)

        self.response.status = 200

