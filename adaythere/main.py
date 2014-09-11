#!/usr/bin/env python

"""
    All user requests to adaythere.com should come to this handler.
    This is the main handler for the application and sets up the one page app.
"""

from google.appengine.api import users
import webapp2
from app.adaythere import ADayThere
from app.lib.components.loggedin import LoggedInNavView
from app.lib.components.loggedout import LoggedOutNavView
from app.lib.components.sidebar import SidebarHeaderView
from app.lib.components.sidebar import MapSearchView
from app.lib.components.sidebar import PlacesSearchView
from app.lib.components.sidebar import MarkersView
from app.lib.components.sidebar import CreateADayView
from app.lib.components.sidebar import MyDaysView
import app.days
import app.login
import app.profile
import app.admin
import app.photos
import app.keywords
import app.locality_days
import app.user_comments
import app.user
from webapp2_extras import i18n
import os
from app.lib.google.maps import Maps
import logging
import json
import inspect
from app.lib.db.user import User
from app.lib.components.genmodal import Modal, ProfileModal, MarkerModal, AdminProfileModal, AddPhotosModal, BecomeAContributorModal
from app.lib.components.element import Elements
from app.lib.components.day_views import DayDisplay, DayPhotoDisplay, DayInfoDisplay
from app.lib.db.days import Day, DayPhoto
from app.lib.components.day_search import DaySearch

class ToolsHandler (webapp2.RequestHandler):
    def get (self):
        """
            Check and see if the user is logged in through
            google. If so set up logged in view else
            setup not logged in view.
        """

        locale = self.request.GET.get ('locale', 'en_US')
        i18n.get_i18n ().set_locale (locale)

        user = users.get_current_user ()

        adaythere = ADayThere ()
        adaythere.add_meta_tags ([
            { "charset":"UTF-8" },
            { "http-equiv":"X-UA-Compatible", "content":"IE=edge" },
            { "name":"description", "content":"A social media site that celebrates the joys of place." },
            { "name":"viewport", "content":"initial-scale=1"}
        ])

        adaythere.add_links ([
            { "rel":"stylesheet", "href":"css/bootstrap.css" },
            { "rel":"stylesheet", "href":"css/adaythere.css" }
        ])


        maps = Maps ()

        adaythere.add_script_tags_for_body ([
            { "src":"js/jquery-1.11.0-beta2.js" },
            { "src":"js/angular/angular.min.js" },
            { "src":"js/angular/angular-route.min.js" },
            { "src":"js/ui-bootstrap-tpls-0.10.0.min.js" },
            { "src": maps.get_script_src () },
            { "src":"js/adaythere.js" },
            { "src":"https://apis.google.com/js/platform.js", "async":None, "defer":None }
        ])

        db_user = None
        navView = None
        logged_in = False
        if user is None:
            navView = LoggedOutNavView ()
            logging.info ("user not logged in")
        else:
            logging.info ("user nickname: " + str (user.nickname ()));
            logging.info ("user email: " + str (user.email ()));
            logging.info ("user id: " + str (user.user_id ()));
            logging.info ("user federated_identity: " + str (user.federated_identity ()));
            logging.info ("user federated_provider: " + str (user.federated_provider ()));
            logging.info ("user auth_domain: " + str (user.auth_domain ()));
            
            db_user = User.query_user_id (str (user.user_id ()))

            if db_user is None:
                db_user = User.record_from_google_user (user)

            if db_user.banned:
                navView = LoggedOutNavView ()
            else:
                navView = LoggedInNavView (db_user)
                logged_in = True

            
        adminProfileModal = AdminProfileModal ()
        contributorModal = BecomeAContributorModal ()

        sidebar_display = """
                <li id="sidebar_display_menu_item" ng-controller="sidebarDisplayCtrl" style="list-style:none; position:absolute; right:10px; top:5px">
                    <a href ng-show="sidebar_link.map_is_displayed" ng-click="toggle_sidebar ()">
                    {{ sidebar_display.menu_text }}
                    </a>
                </li>
        """

        adaythere.open_element ("header", {"id":"page_header"})
        adaythere.open_element ("h1", {"id":"page_heading"}, "A Day There")
        adaythere.close_element ("h1")
        adaythere.open_element ("nav")
        adaythere.append_to_element (navView.get ())
        adaythere.close_element ("nav")
        adaythere.open_element ("div")
        adaythere.append_to_element (adminProfileModal.get ())
        adaythere.close_element ("div")
        adaythere.open_element ("div")
        adaythere.append_to_element (contributorModal.get ())
        adaythere.close_element ("div")
        adaythere.append_to_element (sidebar_display)
        adaythere.close_element ("header")

        adaythere.open_element ("div", { "ng-controller":"daysSearchCtrl"})
        
        adaythere.open_element ("section", { "id":"welcome_to_left" })
        adaythere.append_to_element ("""
                    <img src="img/logo.png" width="60%"></img>
                    <p><h1 style="font-style:italic;text-align:center;font-size:large;">Celebrating the joys of place.</h3></p>
                """)
        adaythere.close_element ("section")
        
        adaythere.open_element ("section", { "id":"welcome_to_right" })
        adaythere.append_to_element ("""<div id="google_like_main" style="float:right;"> <div class="g-plusone" data-size="medium" data-annotation="inline" data-width="250"></div></div>""")
        adaythere.close_element ("section")

        adaythere.open_element ("section", { "id": "daysearch_overlay" })
        day_search = DaySearch ()
        search_form = day_search.get ()
        adaythere.append_to_element (search_form)
        adaythere.close_element ("section")


        adaythere.open_element ("section", { "id":"find_a_day" })

        adaythere.append_to_element ("""
                    <img src="img/logo.png" width="30%"></img>
                    <p><h1 style="font-style:italic;text-align:center;font-size:large;">Celebrating the joys of place.</h3></p>
                """)

        adaythere.append_to_element (day_search.get_days_display ())
        adaythere.close_element ("section")
    
        adaythere.close_element ("div")

        adaythere.append_to_element (MapTools.map_elements ().get ())

        adaythere.open_element ("footer", {"id":"page_footer"})
        adaythere.open_element ("p", None, "&copy; 2014 SoftSprocket")
        adaythere.close_element ("p")
        adaythere.close_element ("footer")


        self.response.write (adaythere.get ())


class MapTools ():

    @classmethod
    def map_elements (cls):
        logged_in = True
        element = Elements ()
        element.open_element ("section", {"id":"map_section"})\
            .close_element ("section")

        sidebarHeaderView = SidebarHeaderView ()
        mapSearchView = MapSearchView (logged_in)
        placesSearchView = PlacesSearchView (logged_in)
        markersView = MarkersView (logged_in)
        createADayView = CreateADayView (logged_in)
        myDaysView = MyDaysView (logged_in)

        profileModal = ProfileModal ()
        markerModal = MarkerModal ()
        addPhotosModal = AddPhotosModal ()

        element.open_element ("section", {"id":"sidebar_section", "ng-controller":"sidebarCtrl"})\
            .open_element ("header", {"id":"sidebar_heading"})\
            .append_to_element (sidebarHeaderView.get ())\
            .close_element ("header")\
            .append_to_element ("<hr></hr>")\
            .open_element ("tabset", {"justified":"false"})\
            .open_element ("tab", {"heading":"Map Tools"})\
            .open_element ("accordion", {"close-others":"true"})\
            .open_element ("accordion-group",{"heading":"Location"})\
            .append_to_element (mapSearchView.get ())\
            .close_element ("accordion-group")\
            .open_element ("accordion-group", {"heading":"Places"})\
            .append_to_element (placesSearchView.get ())\
            .close_element ("accordion-group")\
            .open_element ("accordion-group", {"heading":"Markers"})\
            .append_to_element (markersView.get ())\
            .close_element ("accordion-group")\
            .close_element ("accordion")\
            .close_element ("tab")\
            .open_element ("tab", {"heading":"Create Day"})\
            .append_to_element (createADayView.get ())\
            .close_element ("tab")\
            .open_element ("tab", {"active":"find_a_day.active", "heading":"My Days"})\
            .append_to_element (myDaysView.get ())\
            .close_element ("tab")\
            .close_element ("tabset")\
            .open_element ("div", {"ng-controller":"profileCtrl"})\
            .append_to_element (profileModal.get ())\
            .close_element ("div")\
            .open_element ("div")\
            .append_to_element (markerModal.get ())\
            .close_element ("div")\
            .open_element ("div")\
            .append_to_element (addPhotosModal.get ())\
            .close_element ("div")\
            .close_element ("section")
        return element



app = webapp2.WSGIApplication ([
    ('/', ToolsHandler),
    ('/tools', ToolsHandler),
    ('/photos', app.photos.PhotosHandler),
    ('/days', app.days.DayHandler),
    ('/login', app.login.LoginHandler),
    ('/logout', app.login.LogoutHandler),
    ('/profile', app.profile.ProfileHandler),
    ('/admin_profiles', app.admin.ProfilesHandler),
    ('/keywords', app.keywords.KeywordHandler),
    ('/locality_days', app.locality_days.LocalityDaysHandler),
    ('/user_comments', app.user_comments.UserCommentsHandler),
    ('/users', app.user.UsersHandler)
], debug=True)

