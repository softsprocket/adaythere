
class Maps:

    def __init__(self, sensor=False):

        self.api_url = "https://maps.googleapis.com/maps/api/js"
        self.app_key = "AIzaSyCFuwTO_6v-1Mut3RHfNSAMNpoKH939g8Q"
        self.sensor = str(sensor).lower()

    def get_script_src(self):

        return self.api_url + "?libraries=places,geometry&key=" + self.app_key + "&sensor=" + self.sensor
    


