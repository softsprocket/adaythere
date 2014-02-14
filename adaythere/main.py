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
import app.places
import app.login
import app.profile
from webapp2_extras import i18n
import os
from app.lib.google.maps import Maps
import logging
import json
import inspect
from app.lib.db.user import User
from app.lib.components.genmodal import Modal, ProfileModal, MarkerModal
from app.lib.components.element import Elements

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
            { "rel":"stylesheet", "href":"css/bootstrap.css" },
            { "rel":"stylesheet", "href":"css/adaythere.css" }
        ])


        maps = Maps()

        adaythere.add_script_tags_for_body([
            { "src":"js/jquery-1.11.0-beta2.js" },
            { "src":"js/angular/angular.min.js" },
            { "src":"js/ui-bootstrap-tpls-0.10.0.min.js" },
            { "src": maps.get_script_src() },
            { "src":"js/adaythere.js" }
        ])

        navView = None
        if user is None:
            navView = LoggedOutNavView()
            logging.info("user not logged in")
        else:
            logging.info("user nickname: " + str(user.nickname()));
            logging.info("user email: " + str(user.email()));
            logging.info("user id: " + str(user.user_id()));
            logging.info("user federated_identity: " + str(user.federated_identity()));
            logging.info("user federated_provider: " + str(user.federated_provider()));
            logging.info("user auth_domain: " + str(user.auth_domain()));

            db_user = User.create_user_record_from_google_user(user)
            navView = LoggedInNavView(db_user)


        adaythere.open_element("header", {"id":"page_header"})\
            .open_element("h1", {"id":"page_heading"}, "A Day There")\
            .close_element("h1")\
            .open_element("nav")\
            .append_to_element(navView.get())\
            .close_element("nav")\
            .close_element("header")

        adaythere.open_element("section", {"id":"map_section"})\
            .close_element("section")

        sidebarHeaderView = SidebarHeaderView();
        mapSearchView = MapSearchView();
        placesSearchView = PlacesSearchView();
        
        profileModal = ProfileModal()
        markerModal = MarkerModal()

        adaythere.open_element("section", {"id":"sidebar_section", "ng-controller":"sidebarCtrl"})\
            .open_element("header", {"id":"sidebar_heading"})\
            .append_to_element(sidebarHeaderView.get())\
            .close_element("header")\
            .append_to_element("<hr></hr>")\
            .open_element("tabset", {"justified":"true"})\
            .open_element("tab", {"heading":"Map Tools"})\
            .open_element("accordion", {"close-others":"false"})\
            .open_element("accordion-group",{"heading":"Location"})\
            .append_to_element(mapSearchView.get())\
            .close_element("accordion-group")\
            .open_element("accordion-group", {"heading":"Places"})\
            .append_to_element(placesSearchView.get())\
            .close_element("accordion-group")\
            .close_element("accordion")\
            .close_element("tab")\
            .open_element("tab", {"heading":"Create A Day"})\
            .close_element("tab")\
            .open_element("tab", {"heading":"Find A Day"})\
            .close_element("tab")\
            .close_element("tabset")\
            .open_element("div", {"ng-controller":"profileCtrl"})\
            .append_to_element(profileModal.get())\
            .close_element("div")\
            .open_element("div")\
            .append_to_element(markerModal.get())\
            .close_element("div")\
            .close_element("section")

        adaythere.open_element("footer", {"id":"page_footer"})\
            .open_element("p", None, "&copy; 2014 SoftSprocket")\
            .close_element("p")\
            .close_element("footer")


        self.response.write(adaythere.get())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/places', app.places.PlacesHandler),
    ('/login', app.login.LoginHandler),
    ('/logout', app.login.LogoutHandler),
    ('/profile', app.profile.ProfileHandler)
], debug=True)
