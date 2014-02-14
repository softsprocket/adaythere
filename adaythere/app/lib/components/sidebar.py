
class SidebarHeaderView:

    def __init__(self):

        self.html = """
            <h3>Tools</h3>
            <h3>Current Locality: {{ location.locality }}</h3>
        """


    def get(self):
        return self.html


class PlacesSearchView:

    def __init__(self):

        self.html = """
            <div>
                <h3>Places Search</h3>
                <h4>Click map to set search location</h4>
                <input type="checkbox" ng-click="show_search_area()">Show search area</input>
                <h5>{{ clicked.locality }}</h5>
                <h5>{{ clicked.address }}</h5>
                <h5>Search for nearby:</h5>
                <span  class="nullable">
                <select ng-model="search.selected_type" ng-options="t for t in types">
                    <option value="">-- choose type (defaults to all) --</option>
                </select>
                </span>
                <button type="button" ng-click="search_places()">Go</button>
                {{ search.selected_type }}
                <ul style="list-style:none">
                <li ng-repeat="item in places_array">
                    <a ng-model="item" ng-click="set_marker_at_place(item)">{{item.name}}</a>
                    <br>{{item.types}}</br>
                </li>
                </ul>
            </div>
        """


    def get(self):
        return self.html

class MapSearchView:

    def __init__(self):

        self.html = """
        <div id="search_util">
            <input id="pac_input" type="text"></input>
            <button type="button" ng-click="centre_map_at()">Go</button>
            <button type="button" ng-click="set_marker_at_place(location)">Add Marker</button>
            <h3>{{ location.address }}</h3>
            <h4>{{ location.latitude }} {{ location.longitude }}</h4>
            <button type="button" ng-click="make_default_location()">Set As Default</button>
        </div>
        """

    def get(self):
        return self.html


