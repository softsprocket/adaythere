from app.lib.components.element import Elements

class DayViewPlaces (Elements):

    def __init__ (self, list_name):
        super (DayViewPlaces, self).__init__ ()

        self.open_element ("fieldset")
        self.append_to_element ("""
            <legend>Places</legend>
                <div class="fieldset_box">
                    <div ng-repeat="place in %(list_name)s.places">
                        <a ng-click="adt_marker_modal.open_marker_modal (place, false, %(list_name)s)">{{place.name}}</a>
                        <button type="button" ng-show="($index == (%(list_name)s.places.length - 1))  && show_route_buttons ($parent.$index)" 
                            ng-click="display_route (%(list_name)s, $parent.$index)">Route</button>
                </div>
            </div>
        """ % { "list_name": list_name })
        
        self.close_element ("fieldset")



class DayViewPhotos (Elements):

    def __init__ (self, list_name):
        super (DayViewPhotos, self).__init__ ()

        self.open_element ("fieldset")
        self.append_to_element ("""
            <legend>Photos</legend>
            <div class="fieldset_box">
                <li ng-repeat="photo in %(list_name)s.photos">
                    <a ng-init="collapsed=true" ng-click="collapsed=!collapsed">{{ photo.title }}</a>
                    <div collapse="collapsed">
                        <div class="well well-lg">
                            <img src= "/photos?action=img&title={{ photo.title }}"></img>
                            <legend>Description</legend><input type="text" class="form-control" ng-model="photo.description" ng-disabled="!day_is_editable (%(list_name)s)">    
                        </div> 
                    </div>
                </li>
            </div>

        """ % { "list_name": list_name })

        self.close_element ("fieldset")


class DayViewRater (Elements):

    def __init__ (self, list_name):
        super (DayViewRater, self).__init__ ()

        self.append_to_element ("""
            <button type="button" ng-show="user_comments[$index] ? !user_comments[$index].rated : true" ng-click="open_dayview_rater ($index)">Rate this day!</button>
            <div collapse="user_comments[$index] ? user_comments[$index].collapsed : true">
                <div class="well well-lg">
                    <rating id="daysearch_return_rating" value="user_comments[$index].rating" max="10"></rating><br/>
                    <label for="daysearch_return_comment">Comments:</label>
                    <textarea id="daysearch_return_comment" rows="4" cols="50" ng-model="user_comments[$index].text"></textarea><br/>
                    <button type="button" ng-click="save_user_comment (%(list_name)s, $index)">Save</button>
                    <button type="button" ng-click="cancel_user_comment ($index)">Cancel</button>
                </div>
            </div>
        """ % { "list_name": list_name });


