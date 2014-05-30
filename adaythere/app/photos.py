import webapp2
import json
from app.lib.db.photos import Photos
import logging
from app.lib.db.user import User
from app.adaythere import ADayThere
from google.appengine.ext import ndb

class PhotosHandler (webapp2.RequestHandler):

    def put (self):

        tool_user, db_user = ADayThere.tool_user ()
        if not tool_user:
            self.response.status = 401
            return

        data = self.request.body
        lst = json.loads (data)
        entities = []
        for p in lst:
            photo = Photos ()
            photo.user_id = db_user.user_id
            photo.title = p['title']
            decoded = p['url'].decode ('base64')
            photo.photo = decoded
            entities.append (photo)
        
        ndb.put_multi (entities)
        
        self.response.status = 200


    def get (self):

        tool_user, db_user = ADayThere.tool_user ()
        if not tool_user:
            self.response.status = 401
            return

        action = self.request.get ('action');

        if action is None:
            self.response.status = 401
            return

        if (action == 'count'):
            count = 0
            query = Photos.query_user_id (db_user.user_id)
            if query is not None:
                count = query.count ()

            res = json.dumps ({ "count": count })
            self.response.write (res)
            return
        
        elif (action == 'img'):
            title = self.request.get ('title', None)
            if title is None:
                self.response.status = 401
                return

            photo_query = Photos.query_photo (db_user.user_id, title)
            photo = photo_query.get ()
            
            if photo is None:
                self.response.status = 404
                return

            self.response.headers['Content-Type'] = 'image/png'
            self.response.write (photo.photo)
            return

        elif (action == 'list'):
            list_query = Photos.query_user_id (db_user.user_id)
            
            if list_query is None:
                self.response.status = 404
                return

            titles = []
            photos = list_query.fetch ()
            for photo in photos:
                d = {}
                d['title'] = photo.title;
                d['used_by'] = photo.used_by;
                titles.append (d)

            self.response.write (json.dumps (titles))
            return

  
    def delete (self):

        tool_user, db_user = ADayThere.tool_user ()
        if not tool_user:
            self.response.status = 401
            return

        titlestr = self.request.get ("titles", None)
        used_by = self.request.get ("used_by", None)
        if titlestr is None:
            self.response.status = 401
            return 

        titles = titlestr.split (",")

        if used_by is not None:
            photos = Photos.query (Photos.user_id == db_user.user_id, Photos.title.IN (titles), Photos.used_by == used_by).fetch (keys_only=True)
        else:
            photos = Photos.query (Photos.user_id == db_user.user_id, Photos.title.IN (titles)).fetch (keys_only=True)

        ndb.delete_multi (photos)

        
