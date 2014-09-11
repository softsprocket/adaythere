
import webapp2
import json
from app.lib.db.days import Day
from google.appengine.datastore.datastore_query import Cursor
import hashlib 

class LocalityDaysHandler (webapp2.RequestHandler):

    def get (self):

        rand = self.request.get ('random', None)
        if rand is not None:
            days = Day.query_random (20)
            self.return_days (days, None, False)    
            return

        print 'Here'
        userid = self.request.get ('user_id', None)
        if userid is not None:
            title = self.request.get ('title', None)

            if title is not None:
                day = Day.query_user_title (userid, title).get ()
                print 'day >>>>>>>>', day
                days = []
                days.append (day)
            else:
                days = Day.query_user (userid).fetch ()
                
            self.return_days (days, None, False)
            return


        wordstr = self.request.get ('words', None)
        words = None

        if wordstr is not None:
            if wordstr.find (',') != -1:
                words = wordstr.split (',')
            else:
                words = wordstr.split (' ')

        args = {}

        args['limit'] = self.request.get ('limit', 20)
        
        if self.request.get ('full_locality', None) is not None:
            args['full_locality'] = self.request.get ('full_locality')
        if self.request.get ('cursor', None)  is not None:
            args['cursor'] = Cursor (urlsafe = self.request.get ('cursor'))
        if self.request.get ('user_id', None)  is not None:
            args['user_id'] = self.request.get ('user_id')
        if self.request.get ('minimum_rating', None)  is not None:
            args['minimum_rating'] = int (self.request.get ('minimum_rating'))
        if self.request.get ('all_words', None) is not None:
            args['all_words'] = self.request.get ('all_words')

        keywords = self.request.get ('keywords', None)

        keyhash = None
        if keywords is not None:
            word_list = sorted (map (lambda x: x.strip (), keywords.split (',')))
            keyhash = hashlib.sha256 (str (word_list)).hexdigest ()
       
        if keyhash is None:
            if words is None:
                days, cursor, more = Day.query_days (args)
            else:
                days, cursor, more = Day.query_word_days (args, words)
        else:
            days, cursor, more = Day.query_keyword_days (keyhash, args, words)

        if cursor is not None:
            cursor = cursor.urlsafe ()

        self.return_days (days, cursor, more)


    def return_days (self, days, cursor, more):
        json_days = []
        for each in days:
            json_days.append (json.dumps (each.to_dict ()))

        return_vals= {
            'days': json_days,
            'cursor': cursor,
            'more': more
        };
        
        self.response.status = 200 
        self.response.write (json.dumps (return_vals))
                        

                
