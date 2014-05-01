import webapp2
import json
from app.lib.db.photos import Photos
import logging
from app.lib.db.user import User
from app.adaythere import ADayThere

class PhotosHandler(webapp2.RequestHandler):

    def put(self):

        tool_user, db_user = ADayThere.tool_user()
        if not tool_user:
            self.response.status = 401
            return

        
        photo = Photos()
        photo.userid = db_user.user_id
        photo.day_title = self.request.get('day_title')
        photo.photo_title = self.request.get('photo_title')
        photo.photo = self.request.body

        if photo.day_title is None or photo.photo_title is None or photo.photo is None:
            self.response.status = 400
            return

        
