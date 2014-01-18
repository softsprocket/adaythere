
class SidebarHeaderView:

    def __init__(self):

        self.html = """
            <h3>Map Center</h3>
            <h3>{{ location.locality }}</h3>
            <h3>{{ location.address }}</h3>
            <h4>{{ location.latitude }} {{ location.longitude }}</h4>
        """


    def get(self):
        return self.html


class PlacesSearchView:

    def __init__(self):

        self.html = """
            <div>
                <h3>Places Search</h3>
                <h4>Click map to set search location</hd>
                <h5>{{ clicked.locality }}</h5>
                <h5>{{ clicked.address }}</h5>
                <h5>Search for nearby:</h5>
                <select ng-model="type" ng-options="t for t in types">
                    <option value="">-- choose type (defaults to all) --</option>
                </select>
                <button type="button" ng-click="search_places()">Go</button>
            </div>
        """


    def get(self):
        return self.html

class MapSearchView:

    def __init__(self):

        self.html = """
        <div id="search_util">
            <input id="pac_input" type="text"></input>
            <button type="button" ng-click="go()">Go</button>
        </div>
        """

    def get(self):
        return self.html


