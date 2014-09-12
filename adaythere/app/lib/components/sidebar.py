from app.lib.components.element import Elements
from app.lib.components.day_view_elements import DayViewPlaces, DayViewPhotos

class SidebarHeaderView:

    def __init__ (self):

        self.html = """
            <h3>Tools</h3>
            <h3>Current Locality: {{ location.locality }}</h3>
        """


    def get (self):
        return self.html


class PlacesSearchView:

    def __init__ (self, logged_in):

        if logged_in:
            self.html = """
                <div>
                    <h3>Places Search</h3>
                    <h4>Click map to set search location</h4>
                    <input type="checkbox" ng-click="show_search_area ()">Show search area</input>
                    <h5>{{ clicked.locality }}</h5>
                    <h5>{{ clicked.address }}</h5>
                    <h5>Search for nearby:</h5>
                    <span  class="nullable">
                    <select ng-model="search.selected_type" ng-options="t for t in types">
                        <option value="">-- choose type (defaults to all) --</option>
                    </select>
                    </span>
                    <button type="button" ng-click="search_places ()">Go</button>
                    {{ search.selected_type }}
                    <ul style="list-style:none">
                    <li ng-repeat="item in places_array">
                        <a ng-model="item" ng-click="set_marker_at_place (item)">{{item.name}}</a>
                        <br>{{item.types}}</br>
                    </li>
                    </ul>
                </div>
            """
        else:
            self.html = """
                <h3>Please log in for access to map tools</h3>
            """

    def get (self):
        return self.html

class MapSearchView:

    def __init__ (self, logged_in):

        if logged_in:
            self.html = """
            <div id="location_search_util">
                <input id="autocomplete_google_input" type="text"></input>
                <button id="centre_map_at_button" type="button" ng-click="centre_map_at ()">Go</button>
                <button type="button" ng-click="set_marker_at_place (location)">Add Marker</button>
                <h3>{{ location.vicinity }}</h3>
                <h4>{{ location.latitude }} Lat. {{ location.longitude }} Lon.</h4>
                <button type="button" ng-click="make_default_location ()">Set As Default</button>
            </div>
            """
        else:
            self.html = """
                <h3>Please log in for access to map tools</h3>
            """

    def get (self):
        return self.html


class MarkersView:

    def __init__ (self, logged_in):

        if logged_in:
            self.html = """
            <div id="makers_util">
                <button type="button" ng-click="adt_markers.clear_all_markers ()">Clear All Markers</button>
                <li ng-repeat="marker in adt_markers.markers">
                    <a ng-click="adt_marker_modal.open_marker_modal (marker)">{{marker.name}}</a>
                    <button type="button" ng-click="adt_remove_marker (marker)">Remove</button>
                </li>
            </div>
            """
        else:
            self.html = """
                <h3>Please log in for access to map tools</h3>
            """

    def get (self):
        return self.html

class CreateADayView:

    def __init__ (self, logged_in):
        if logged_in:
            self.html = """
            <form>
            <fieldset style="padding:6px">
                <label>Locality: {{ current_created_day.full_locality }} </label><br> 
                <label for="creation_title">Title</label>
                <input id="creation_title" class="form-control" type='text' ng-model='current_created_day.title'></input>
                <label for="creation_keywords">Keywords</label>
                <input id="creation_keywords" class="form-control" type='text' ng-model='current_created_day.keywords' data-role='tagsinput'></input>
                <label for="creation_descrip">Comments</label>
                <textarea id="creation_descrip"  class="form-control" ng-model='current_created_day.description'></textarea>
                <fieldset>
                    <legend>Places</legend>
                    <div class="fieldset_box">
                        <li ng-repeat="place in current_created_day.places">
                            <a ng-click="adt_marker_modal.open_marker_modal (place, false)">{{place.name}}</a>
                            <button type="button" ng-disabled="top_places_list (place)" ng-click="creation_moveup (place)">Up</button>
                            <button type="button" ng-disabled="bottom_places_list (place)" ng-click="creation_movedown (place)">Down</button>
                        </li>
                    </div>
                </fieldset>
                <fieldset>
                    <legend>Photos</legend>
                    <div class="fieldset_box">
                        <li ng-repeat="photo in current_created_day.photos">
                            <a ng-init="collapsed=true" ng-click="collapsed=!collapsed">{{ photo.title }}</a>
                            <div collapse="collapsed">
                                <div class="well well-lg">
                                    <img src= "/photos?action=img&title={{ photo.title }}"></img>
                                    <legend>Description</legend><input type="text" class="form-control" ng-model="photo.description">
                                </div> 
                            </div>
                                                                                    
                        </li>
                    </div>
                </fieldset>
                <button id="creation_save_button" type="button" ng-click="creation_save ()">Save</button>
                <button id="creation_clear_button" type="button" ng-click="creation_clear (true)">Clear</button>
                <button id="creation_photo_button" type="button" ng-click="open_add_photo_modal ()">Add photos</button>
            </fieldset>
            </form>
            """
        else:
            self.html = """
                <h3>Please log in to create your own days.</h3>
            """

    def get (self):
        return self.html


class MyDaysView:

    def __init__ (self, logged_in):
        if logged_in:
            element = Elements () 
            element.open_element ("accordion", {"close-others":"true"})
            
            element.open_element ("accordion-group",{"heading":"Saved Days", "is-open":"true"})
            element.append_to_element ("""
                <div class="ng-cloak" ng-show='my_days.length > 0'><input id="my_days_expander" type='button' value="Expand All" ng-click='my_days_expand ()'></input></div>
                <li ng-repeat="day in my_days">
                    <a ng-click="my_day_toggle_open (day)">{{ day.title }}</a>
                    <button type="button" ng-click="delete_day (day)">Delete</button>
                    <div collapse="day.is_collapsed">
                        <div class="well well-lg">
                            <label>Locality: {{ day.full_locality }} </label><br>
                            <label for="day_keywords">Keywords</label>
                            <input id="day_keywords" class="form-control" type='text' ng-disabled="!day_is_editable (day)" ng-model='day.keywords' data-role='tagsinput'></input>
                            <label for="day_description">Description</label>
                            <input id="day_description" class="form-control" type='text' ng-disabled="!day_is_editable (day)" ng-model='day.description'></input>
            """)

            dayview_places = DayViewPlaces ("day")
            element.append_to_element (dayview_places.get ())
            dayview_photos = DayViewPhotos ("day")
            element.append_to_element (dayview_photos.get ())

            element.append_to_element ("""
                            <button type="button" ng-disabled="day_is_editable (day)" ng-click="set_day_editable (day, $index)">Edit</button>
                            <button type="button" ng-disabled="!day_is_editable (day)" ng-click="save_modified_day (day)">Save</button>
                            <button type="button" ng-disabled="day_is_editable (day)" ng-click="copy_day_as (day)">Copy As</button>
                            <button type="button" ng-disabled="!day_is_editable (day)" ng-click="cancel_changes_to_day (day)">Cancel</button>
                            <input id="display_day_view_button_{{ $index }}" type="button" ng-click="display_day_view (day, $index)" value="Display"></input>
                            <select ng-model="direction_mode[$index]" ng-options="mode for mode in direction_modes">
                            </select>
                        </div> 
                    </div>
                </li>
            """)
            element.close_element ("accordion-group")
            
            element.open_element ("accordion-group",{"heading":"Deleted Days", "is-open":"false"})
            element.append_to_element ("""
                    <div class="ng-cloak" ng-show='my_deleted_days.length > 0'>
                        <input id="my_deleted_days_expander" type='button' value="Expand All" ng-click='my_deleted_days_expand ()'></input>
                    </div>
                    <li ng-repeat="day in my_deleted_days">
                        <a ng-click="my_day_toggle_open (day)">{{ day.title }}</a>
                        <button type="button" ng-click="restore_day (day)">Restore</button>
                        <div collapse="day.is_collapsed">
                            <div class="well well-lg">
                                <label>Locality: {{ day.full_locality }} </label><br>
                                <label for="deleted_day_keywords">Keywords</label>
                                <input id="deleted_day_keywords" class="form-control" type='text' ng-disabled="!day_is_editable (day)" ng-model='day.keywords' data-role='tagsinput'></input>
                                <label for="deleted_day_description">Description</label>
                                <input id="deleted_day_description" class="form-control" type='text' ng-disabled="!day_is_editable (day)" ng-model='day.description'></input>
            """)

            dayview_places = DayViewPlaces ("day")
            element.append_to_element (dayview_places.get ())
            dayview_photos = DayViewPhotos ("day")
            element.append_to_element (dayview_photos.get ())
            
            element.append_to_element ("""
                                <input id="display_day_view_button_{{ $index }}" type="button" ng-click="display_day_view (day, $index)" value="Display"></input>
                                <select ng-model="direction_mode[$index]" ng-options="mode for mode in direction_modes">
                                </select>
                            </div> 
                        </div>
                    </li>
            """)
            element.close_element ("accordion-group")
            element.close_element ("accordion")

            self.html = element.get ()
        else:
            self.html = """

            """

    def get (self):
        return self.html


