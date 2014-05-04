import webapp2
import json
from app.lib.db.photos import Photos
import logging
from app.lib.db.user import User
from app.adaythere import ADayThere
from google.appengine.ext import ndb

class PhotosHandler(webapp2.RequestHandler):

    def put(self):

        tool_user, db_user = ADayThere.tool_user()
        if not tool_user:
            self.response.status = 401
            return

        data = self.request.body
        lst = json.loads (data)
        entities = []
        for p in lst:
            photo = Photos()
            photo.user_id = db_user.user_id
            photo.title = p['title']
            photo.photo = p['url']
            entities.append(photo)
        
        ndb.put_multi(entities)

        
        count = 0
        query = Photos.query_user_id(db_user.user_id)

        if query is not None:
            count = query.count()
        
        res = json.dumps({ "count": count })
        self.response.write(res)


    def get(self):

        tool_user, db_user = ADayThere.tool_user()
        if not tool_user:
            self.response.status = 401
            return

        action = self.request.get ('action');

        if (action == 'count'):
            count = 0
            query = Photos.query_user_id(db_user.user_id)
            if query is not None:
                count = query.count()

            res = json.dumps({ "count": count })
            self.response.write(res)
            return





