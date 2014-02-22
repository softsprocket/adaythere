from app.lib.components.element import Elements

class SidebarHeaderView:

    def __init__(self):

        self.html = """
            <h3>Tools</h3>
            <h3>Current Locality: {{ location.locality }}</h3>
        """


    def get(self):
        return self.html


class PlacesSearchView:

    def __init__(self, logged_in):

        if logged_in:
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
        else:
            self.html = """
                <h3>Please log in for access to map tools</h3>
            """

    def get(self):
        return self.html

class MapSearchView:

    def __init__(self, logged_in):

        if logged_in:
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
        else:
            self.html = """
                <h3>Please log in for access to map tools</h3>
            """

    def get(self):
        return self.html


class MarkersView:

    def __init__(self, logged_in):

        if logged_in:
            self.html = """
            <div id="makers_util">
                <button type="button" ng-click="clear_all_markers()">Clear All Markers</button>
                <li ng-repeat="marker in markers">
                    <a ng-click="open_marker_modal(marker, true)">{{marker.name}}</a>
                    <button type="button" ng-click="remove_marker(marker)">Del</button>
                </li>
            </div>
            """
        else:
            self.html = """
                <h3>Please log in for access to map tools</h3>
            """

    def get(self):
        return self.html

class CreateADayView:

    def __init__(self, logged_in):
        if logged_in:
            self.html = """
                <label for="creation_title">Title</label>
                <input id="creation_title" class="form-control" type='text' ng-model='current_creation_day.title'></input>
                <label for="creation_descrip">Description</label>
                <textarea id="creation_descrip"  class="form-control" ng-model='current_creation_day.description'></textarea>
                <label for="creation_places_list">List of Places</label>
                <li id:"creation_places_list" ng-repeat="place in current_creation_day.places">
                    <a ng-click="open_marker_modal(place, false)">{{place.name}}</a>
                    <button ng-show="not_top_places_list(place)" type="button" ng-click="creation_moveup(place)">Up</button>
                    <button ng-show="not_bottom_places_list(place)" type="button" ng-click="creation_movedown(place)">Down</button>
                    <button type="button" ng-click="creation_remove(place)">Del</button>
                </li>
                <alert ng-repeat="alert in creationralerts" type="alert.type" close="creation_close_alert($index)">{{alert.msg}}</alert>
                <button type="button" ng-click="creation_save()">Save</button>
                <button type="button" ng-click="creation_clear()">New</button>

            """
        else:
            self.html = """
                <h3>Please log in to create your own days.</h3>
            """

    def get(self):
        return self.html


class FindADayView:

    def __init__(self, logged_in):
        if logged_in:
            element = Elements () 
            element.open_element("accordion", {"close-others":"true"})\
                .open_element("accordion-group",{"heading":"My Days"})\
                .append_to_element("""
                    <li ng-repeat="day in my_days">
                        <a ng-click=edit_saved_day(day)>{{day.title}}</a>
                    </li>
                """)\
                .close_element("accordion-group")\
                .open_element("accordion-group", {"heading":"Other Days"})\
                .append_to_element("""
                
                """)\
                .close_element("accordion-group")\
                .close_element("accordion")

            self.html = element.get ()
           
        else:
            self.html = """"edit_my_day(day)"

            """

    def get(self):
        return self.html


