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
from app.placeshandler import PlacesHandler
from webapp2_extras import i18n
import os
from app.lib.google.maps import Maps


class MainHandler(webapp2.RequestHandler):
    def get(self):
        """
            Check and see if the user is logged in through
            google. If so set up logged in view else
            setup not logged in view. 
        """

        locale = self.request.GET.get('locale', 'en_US')
        i18n.get_i18n().set_locale(locale)

        user = users.get_current_user()

        adaythere = ADayThere()
        adaythere.add_meta_tags([
            { "charset":"UTF-8" },
            { "http-equiv":"X-UA-Compatible", "content":"IE=edge" },
            { "name":"description", "content":"A social media site that celebrates the joys of place." },
            { "name":"viewport", "content":"initial-scale=1"}    
        ])
       
        adaythere.add_links([
            { "rel":"stylesheet", "href":"css/adaythere.css" }
        ])


        maps = Maps()

        adaythere.add_script_tags_for_body([
            { "src":"js/jquery-1.11.0-beta2.js" },
            { "src":"js/angular/angular.min.js" },
            { "src": maps.get_script_src() },
            { "src":"js/adaythere.js" }
        ])

        navView = None
        if user is None:
            navView = LoggedOutNavView()
        else:
            navView = LoggedInNavView(user)

        adaythere.open_element("header", {"id":"page_header"})\
            .open_element("h1", {"id":"page_heading"}, "A Day There")\
            .close_element("h1")\
            .open_element("nav", { "id":"top_nav" })\
            .append_to_element(navView.get())\
            .close_element("nav")\
            .close_element("header")

        adaythere.open_element("section", {"id":"map_section"})\
            .close_element("section")

        sidebarHeaderView = SidebarHeaderView();
        mapSearchView = MapSearchView();
        placesSearchView = PlacesSearchView();
        adaythere.open_element("section", {"id":"sidebar_section", "ng-controller":"sidebarCtrl"})\
            .open_element("header", {"id":"sidebar_heading"})\
            .append_to_element(sidebarHeaderView.get())\
            .close_element("header")\
            .append_to_element(mapSearchView.get())\
            .append_to_element(placesSearchView.get())\
            .close_element("section")

        adaythere.open_element("footer", {"id":"page_footer"})\
            .open_element("p", None, "&copy; 2014 SoftSprocket")\
            .close_element("p")\
            .close_element("footer")

        print os.environ;

        self.response.write(adaythere.get())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/places', PlacesHandler)
], debug=True)
