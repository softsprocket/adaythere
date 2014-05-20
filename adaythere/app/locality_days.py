
import webapp2
import json
from app.lib.db.keywords import KeywordsDayList

class LocalityDaysHandler(webapp2.RequestHandler):

    def get (self):

        locality = self.request.get('locality')
        page_limit = self.request.get('limit')
        page_cursor = self.request.get('cursor')
        str_keywords = self.request.get('keywords')
        
        keywords = str.keywords.split (",");

        keyhash = hash(str(sorted(keywords)))
        kdl_query = KeywordsDayList.query_keyhash(keyhash, locality)

        options = {}

        if page_cursor is not None:
            options['cursor'] = Cursor(page_cursor)

        return_vals = {}
        return_vals['results'], return_vals['cursor'], return_vals['more'] = kdl_query.fetch_page(limit, options)


                
        
                
