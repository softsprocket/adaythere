from app.lib.components.element import Elements
from app.lib.components.day_view_elements import DayViewPlaces, DayViewPhotos, DayViewRater

class DaySearch (Elements):

    def __init__(self):
        super (DaySearch, self).__init__()


        self.open_element ("form", {"class": "simple-form"})
        self.open_element ("fieldset", {"class": "fieldset_box fieldset_daysearch"})
        self.append_to_element ("<legend>Day Search</legend>")

        self.append_to_element ("""
            <p><label class="daysearch_label" for="locality_autocomplete_input">Locality:</label>
            <input id="locality_autocomplete_input" type="text" placeholder="Enter a locality" autocomplete="off" ng-model="daysearch.full_locality" class="daysearch_input"></input>  
        """)

        self.append_to_element ("""
            <p><label class="daysearch_label" for="daysearch_words_input">Search terms:</label>
            <input id="daysearch_words_input" type="text" placeholder="Enter search words" ng-model="daysearch.words" class="daysearch_input"></input>
        """)

        self.append_to_element ("""
            <p><label class="daysearch_label" for="daysearch_rating">Minimum rating:</label>
            <rating id="daysearch_rating" value="daysearch.rating" max="daysearch.max"></rating>
        """)

        self.append_to_element ("""
            <p><label class="daysearch_label" for="daysearch_all_words_radio">All words:</label>
            <input id="daysearch_all_words_radio" type="radio" ng-model="daysearch.all_words" value="all"></input>
            <p><label class="daysearch_label" for="daysearch_any_words_radio">Any words:</label>
            <input id="daysearch_any_words_radio" type="radio" ng-model="daysearch.all_words" value="any"></input>
        """)

        self.append_to_element ("""
            <p><label class="daysearch_label">Keywords:</label>
            <select multiple ng-model="daysearch.selected_keywords" ng-options="keyword for keyword in daysearch.keywords">
                <option value="">--Choose keywords--</option>
            </select>
        """)

        self.append_to_element ("""
            <p>
            <button ng-click="executeSearch()">Search</button>
            <button ng-click="getRandomDays()" style="float:right;">Random Days</button>
        """)

        self.close_element ("fieldset")
        self.close_element ("form")

    
    def get_days_display (self):
        elements = Elements ();
        elements.open_element ("div", { "id":"daysearch_return_display" })
        elements.append_to_element ("""<h1 class="heading_font">{{ daysearch_returned.msg_to_user }}</h1>""")
        elements.open_element ("li", { "ng-repeat":"day in daysearch_returned.days" });
        elements.append_to_element ("""
                    <a ng-click="day_toggle_open (day)">{{ day.title }}</a>
                    <p>{{ day.description }}</p>
                    <div collapse="day.is_collapsed">
                        <div class="well well-lg">
                            <div class="g-plus" data-action="share" data-href="//adaythere.com/locality_days?user_id={{ day.userid }}&title={{ day.title }}></div>
                            <label>Locality: {{ day.full_locality }} </label><br>
                            <label for="day_keywords">Keywords</label>
                            <input id="day_keywords" class="form-control" type='text' ng-disabled="true" ng-model='day.keywords'></input>
                            <label for="day_description">Description</label>
                            <input id="day_description" class="form-control" type='text' ng-disabled="!day_is_editable (day)" ng-model='day.description'></input>
        """)

        dayview_places = DayViewPlaces ("day")
        elements.append_to_element (dayview_places.get ())
        dayview_photos = DayViewPhotos ("day")
        elements.append_to_element (dayview_photos.get ())

        elements.append_to_element ("""
            <p>Posted by: {{ day.name }} </p>
            Number of reviews: {{day.numberOfReviews}} - Average review: <rating value="day.averageReview" max="10"></rating>
            <a ng-click="show_reviews_for ($index)" style="float: right;">Reviews</a>
            <br>
            <div id="daysearch_review_display_window{{$index}}" style="display:none; z-index:20; width:50%; height:50%; overflow-y:auto;" >
                <div ng-repeat="review in daysearch_returned.reviews[$index]">
                    <p>Posted by: {{ review.commenters_id }}</p>
                    <rating value="review.rating" max="10"></rating><br/>
                    <p>{{ review.text }}</p><br/>
                </div>
            </div>
            <button id="dayssearch_show_map_button{{$index}}" type="button" ng-click="show_map_of (day, $index)">View Map</button>
            <button ng-click="open_google_plus_window (day.userid, day.title)">Share
                <img src="https://www.gstatic.com/images/icons/gplus-16.png" alt="Share on Google+"/>
            </button>
        """)

        dayview_rater = DayViewRater ("day")
        elements.append_to_element (dayview_rater.get ())

        elements.append_to_element ("""
                        <select id="daysearch_travelmode_selector{{$index}}" ng-model="direction_mode[$index]" ng-options="mode for mode in direction_modes" style="display:none">
                        </select>

                        <div id="googlemap_of_{{$index}}"><div>
                        </div> 
                    </div>
        """)
        elements.close_element ("li");
        elements.append_to_element ("""
            <button type="button" ng-click="return_to_daysearch ()">Search Again</button>
        """);
        elements.close_element ("div");
        
        return elements.get ()


    def get (self):

        return super (DaySearch, self).get ()

