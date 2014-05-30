
import webapp2
import json
from app.lib.db.days import Day
from google.appengine.datastore.datastore_query import Cursor
import hashlib 
class LocalityDaysHandler (webapp2.RequestHandler):

    def get (self):

        args = {}

        args['limit'] = self.request.get ('limit', None)
        if args['limit'] is None:
            args['limit'] = 20
        
        if self.request.get ('locality', None) is not None:
            args['locality'] = self.request.get ('locality')
        if self.request.get ('cursor', None)  is not None:
            args['cursor'] = Cursor (urlsafe = self.request.get ('cursor'))
        if self.request.get ('user_id', None)  is not None:
            args['user_id'] = self.request.get ('user_id')
        if self.request.get ('minimum_rating', None)  is not None:
            args['minimum_rating'] = self.request.get ('minimum_rating')

        keywords = self.request.get ('keywords', None)


        keyhash = None
        if keywords is not None:
            word_list = sorted (map (lambda x: x.strip (), keywords.split (',')))
            keyhash = hashlib.sha256(str(word_list)).hexdigest()


        if keyhash is None:
            days, cursor, more = Day.query_days (args)
        else:
            days, cursor, more = Day.query_keyword_days (keyhash, args)

        if cursor is not None:
            cursor = cursor.urlsafe ()
      
        json_days = []
        for each in days:
            json_days.append (json.dumps (each.to_dict ()))

        return_vals= {
            'days': json_days,
            'cursor': cursor,
            'more': more
        };

        self.response.write (json.dumps (return_vals))
                        

                
