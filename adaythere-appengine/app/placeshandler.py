"""
    Request handler for /places
"""

import webapp2
import json
from app.lib.components.twitterplaces import QueryModel
import logging

class PlacesHandler(webapp2.RequestHandler):

    def get(self):
        """
            Responds to a get request.
        """

        place = self.request.get('place')

        logging.info("Getting %s", place)

        queryModel = QueryModel(place)
        result, data = queryModel.get()
       
        if result:
            parsed_data = json.loads(data)
            places = parsed_data['result']['places']
            
            self.response.write(json.dumps(places))
        else:
            self.response.write("Unable to get " + place) 


