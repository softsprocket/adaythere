import app.lib.db.places
from uuid import uuid4

class PlaceModel:

    def __init__(self, placeId):

        if placeId is None:
            self.placeId = uuid4()
        else:
            self.placeId = placeId



    def get(self):
        return Place.query_id(self.placeId)


    def set(self, place):
        pass



