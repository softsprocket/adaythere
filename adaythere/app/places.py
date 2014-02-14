"""
    Request handler for /places
"""

import webapp2
import json
import app.lib.components.places
import logging

class PlacesHandler(webapp2.RequestHandler):

    def get(self):
        """
            Responds to a get request.
        """

        placeId = self.request.get('placeId')

        logging.info("Getting %s", placeId)

        queryModel = QueryModel(placeId)
        place = queryModel.get()
       
        if place is not None:
            self.response.write(json.dumps(place))
        else:
            self.response.write("Unable to get " + placeId) 


