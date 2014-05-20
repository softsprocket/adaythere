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
from webapp2_extras import i18n
import os
from app.lib.google.maps import Maps
import logging
import json
import inspect
from app.lib.db.user import User
from app.lib.components.genmodal import Modal, ProfileModal, MarkerModal, SelectDayModal, AdminProfileModal, AddPhotosModal
from app.lib.components.element import Elements

class ToolsHandler(webapp2.RequestHandler):
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

        db_user = None
        navView = None
        logged_in = False
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

            db_user = User.query_user_id(str(user.user_id()))

            if db_user is None:
                db_user = User.record_from_google_user(user)

            if db_user.banned:
                navView = LoggedOutNavView()
            else:
                navView = LoggedInNavView(db_user)
                logged_in = True


        adminProfileModal = AdminProfileModal()


        sidebar_display = """
                <li id="sidebar_display_menu_item" ng-controller="sidebarDisplayCtrl" style="list-style:none; position:absolute; right:10px; top:5px">
                    <a href ng-show="sidebar_link.map_is_displayed" ng-click="toggle_sidebar ()">
                    {{ sidebar_display.menu_text }}
                    </a>
                </li>
        """

        adaythere.open_element("header", {"id":"page_header"})\
            .open_element("h1", {"id":"page_heading"}, "A Day There")\
            .close_element("h1")\
            .open_element("nav")\
            .append_to_element(navView.get())\
            .close_element("nav")\
            .open_element("div")\
            .append_to_element(adminProfileModal.get())\
            .close_element("div")\
            .append_to_element(sidebar_display)\
            .close_element("header")

        adaythere.open_element("section", { "id":"welcome_to_left", "ng-controller":"welcome_controller"})\
            .append_to_element("""
                    <button type="button" ng-click="open_welcome_doors()" style="position:absolute;right:0">Click</button>
                """)\
            .close_element("section")

        adaythere.open_element("section", { "id":"welcome_to_right", "ng-controller":"welcome_controller" })\
            .append_to_element("""
                    <button type="button" ng-click="open_welcome_doors()" style="position:absolute;left:0">Me</button>
                """)\
            .close_element("section")

        adaythere.open_element("section", { "id":"find_a_day", "ng-controller":"find_a_day_controller" })\
            .append_to_element("""
                    <button type=button ng-click="become_a_contributor()" style="position:absolute;bottom:0">Get Access To Tools</button>
                """)\
            .close_element("section")

        adaythere.append_to_element(MapTools.map_elements().get())

        adaythere.open_element("footer", {"id":"page_footer"})\
            .open_element("p", None, "&copy; 2014 SoftSprocket")\
            .close_element("p")\
            .close_element("footer")


        self.response.write(adaythere.get())

class HomeHandler(webapp2.RequestHandler):
    def get(self):

        adaythere = ADayThere()
        adaythere.add_meta_tags([
            { "charset":"UTF-8" },
            { "http-equiv":"X-UA-Compatible", "content":"yes" },
            { "name":"apple-mobile-web-app-capable", "content":"A social media site that celebrates the joys of place." },
            { "name":"viewport", "content":"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" },
            { "name":"description", "content":"A social media site that celebrates the joys of place." },
            { "name":"viewport", "content":"initial-scale=1"}
        ])

        adaythere.add_links([
            { "rel":"stylesheet", "href":"css/bootstrap.css" },
            { "rel":"stylesheet", "href":"css/flat-ui.css" },
            { "rel":"stylesheet", "href":"css/icon-font.css" },
            { "rel":"stylesheet", "href":"css/animations.css" },
            { "rel":"stylesheet", "href":"css/home.css" }
        ])


        maps = Maps()

        adaythere.add_script_tags_for_body([
            { "src":"js/jquery-1.11.0-beta2.js" },
            { "src":"js/angular/angular.min.js" },
            { "src":"js/ui-bootstrap-tpls-0.10.0.min.js" },
            { "src":"js/bootstrap.min.js" },
            { "src":"js/flatui-radio.js" },
            { "src":"js/flatui-checkbox.js" },
            { "src":"js/ui-bootstrap-tpls-0.10.0.min.js" },
            { "src":"js/jquery.scrollTo-1.4.3.1-min.js" },
            { "src":"js/modernizr.custom.js" },
            { "src":"js/page-transitions.js" },
            { "src":"js/easing.min.js" },
            { "src":"js/jquery.svg.js" },
            { "src":"js/jquery.svganim.js" },
            { "src":"js/jquery.parallax.min.js" },
            { "src":"js/startup-kit.js" },
            { "src": maps.get_script_src() },
            { "src":"js/home.js"}
        ])

        adaythere.open_element("div", {"class":"page-wrapper"})

        header_display = """
                    <!-- header -->
                    <header class="header">
                        <div class="container">
                            <div class="row">
                                <nav class="navbar col-sm-12 navbar-fixed-top" role="navigation">
                                    <div class="navbar-header">
                                        <button type="button" class="navbar-toggle"></button>
                                        <a class="brand" href="#"><img src="/icons/logo@2x.png" width="260" height="60" alt=""></a>
                                    </div>
                                    <div class="collapse navbar-collapse pull-right">
                                        <ul class="nav pull-left">
                                            <li><a href="#about">ABOUT US</a></li>
                                            <li><a href="#day_search">FIND A DAY</a></li>
                                            <li><a href="/tools">CREATE A DAY</a></li>
                                            <li><a href="#contact">CONTACT</a></li>
                                        </ul>
                                        <form class="navbar-form pull-left">
                                            <a class="btn btn-primary" href="#">SIGN IN</a>
                                        </form>
                                    </div>
                                </nav>
                            </div>
                        </div>
                        <div class="header-background"></div>
                    </header>
                    <section class="header-sub">
                        <div class="background">&nbsp;</div>
                        <div class="container">
                            <div class="row">
                                <div class="col-sm-6">
                                    <h3>Your Day, Your Way</h3>
                                    <p>Let us help you create the perfect day</p>
                                </div>
                            </div>
                        </div>
                    </section>
        """

        adaythere.open_element("header", {"id":"page_header", "ng-controller":"welcome_controller"})\
            .append_to_element(header_display)\
            .close_element("header")

        days_display = """
            <div class="container">
                <h3>
                    Check out these amazing days that people have created.
                </h3>

                <div class="days">
                    <div class="day-wrapper">
                        <div class="day">
                            <div class="photo-wrapper">
                                <div class="photo" style="background-image: url(images/placeholder/img-5.png);"><img alt="" src="images/placeholder/img-5.png" style="display: none;">
                                </div>
                                <div class="overlay">
                                    <span class="fui-eye"> </span>
                                </div>
                            </div>
                            <div class="info">
                                <div class="name">
                                    Day 1
                                </div>
                                Fine dining, Gardens and historic sites.
                            </div>
                        </div>
                    </div>

                    <div class="day-wrapper">
                        <div class="day">
                            <div class="photo-wrapper">
                                <div class="photo" style="background-image: url(images/placeholder/img-5.png);"><img alt="" src="images/placeholder/img-5.png" style="display: none;">
                                </div>
                                <div class="overlay">
                                    <span class="fui-eye"> </span>
                                </div>
                            </div>
                            <div class="info">
                                <div class="name">
                                    Day 2
                                </div>
                                Fine dining, Gardens and historic sites.
                            </div>
                        </div>
                    </div>

                    <div class="day-wrapper">
                        <div class="day">
                            <div class="photo-wrapper">
                                <div class="photo" style="background-image: url(images/placeholder/img-5.png);"><img alt="" src="images/placeholder/img-5.png" style="display: none;">
                                </div>
                                <div class="overlay">
                                    <span class="fui-eye"> </span>
                                </div>
                            </div>
                            <div class="info">
                                <div class="name">
                                    Day 3
                                </div>
                                Fine dining, Gardens and historic sites.
                            </div>
                        </div>
                    </div>
                </div>
                <div class="days">
                    <div class="day-wrapper ani-processed" style="">
                        <div class="day">
                            <div class="photo-wrapper">
                                <div class="photo" style="background-image: url(images/placeholder/img-5.png);"><img alt="" src="images/placeholder/img-5.png" style="display: none;">
                                </div>
                                <div class="overlay">
                                    <span class="fui-eye"> </span>
                                </div>
                            </div>
                            <div class="info">
                                <div class="name">
                                    Day 4
                                </div>
                                Fine dining, Gardens and historic sites.
                            </div>
                        </div>
                    </div>

                    <div class="day-wrapper ani-processed" style="">
                        <div class="day">
                            <div class="photo-wrapper">
                                <div class="photo" style="background-image: url(images/placeholder/img-5.png);"><img alt="" src="images/placeholder/img-5.png" style="display: none;">
                                </div>
                                <div class="overlay">
                                    <span class="fui-eye"> </span>
                                </div>
                            </div>
                            <div class="info">
                                <div class="name">
                                    Day 5
                                </div>
                                Fine dining, Gardens and historic sites.
                            </div>
                        </div>
                    </div>

                    <div class="day-wrapper ani-processed" style="">
                        <div class="day">
                            <div class="photo-wrapper">
                                <div class="photo" style="background-image: url(images/placeholder/img-5.png);"><img alt="" src="images/placeholder/img-5.png" style="display: none;">
                                </div>
                                <div class="overlay">
                                    <span class="fui-eye"> </span>
                                </div>
                            </div>
                            <div class="info">
                                <div class="name">
                                    Day 6
                                </div>
                                Fine dining, Gardens and historic sites.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        """

        adaythere.open_element("section", {"id":"day_search", "class": "day-search"})\
            .append_to_element(days_display)\
            .close_element("section")

        about_display = """
            <div id="pt-2" class="page-transitions pt-perspective">
                <div class="pt-page pt-page-1 pt-page-current bg-clouds">
                    <div class="container">
                        <div class="box-icon">
                            <a class="fui-arrow-left pt-control-prev" href="#"> </a>
                            <span class="icon fui-gear"> </span>
                            <a class="fui-arrow-right pt-control-next" href="#"> </a>
                        </div>
                        <div class="row">
                            <div class="col-sm-6 col-sm-offset-3">
                                <h3>About Us</h3>
                                <div class="article-info">
                                    <span><span class="fui-user"> </span> GREG MARTIN</span>
                                    <span><span class="fui-time"> </span> 20 MAY</span>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-8 col-sm-offset-2">
                                <p style="margin: 0">
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ac tincidunt arcu. Maecenas vel tellus ut magna bibendum elementum. Donec suscipit pharetra ligula id consectetur. Sed id erat orci. Donec nec metus imperdiet tortor pulvinar mattis. Proin ut erat ac est ultrices feugiat. Integer hendrerit ullamcorper tellus, at tempor odio tristique vitae. Curabitur tincidunt risus justo, tristique fermentum quam molestie non. Cras bibendum eget quam quis congue. In suscipit mollis magna id tincidunt. Curabitur sit amet ligula vitae libero auctor ultrices. Nam vitae tortor tristique, tempus nulla ultricies, malesuada augue. Quisque convallis tristique sem, et volutpat enim tempus sed. Ut lobortis pellentesque neque ac feugiat.
                                    <br><br>
                                    Aenean et suscipit ante. Integer malesuada tempus vestibulum. Nulla posuere adipiscing lectus vitae tristique. Proin venenatis sodales laoreet. Nam dictum leo ac nibh porta, vestibulum sollicitudin risus lacinia. Integer ac porta risus, ac feugiat orci. Aliquam malesuada dolor non laoreet convallis. Duis mauris massa, tincidunt et volutpat nec, posuere et ante. Vivamus pulvinar ante vel augue pellentesque sodales. Vestibulum molestie euismod ultrices. Pellentesque nunc diam, commodo sed ligula ultricies, dapibus hendrerit massa. Nam varius tortor tortor, rutrum consequat nibh feugiat eget. Donec aliquet interdum nisl eget vulputate.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="pt-page pt-page-2 bg-clouds">
                    <div class="container">
                        <div class="box-icon">
                            <a class="fui-arrow-left pt-control-prev" href="#"> </a>
                            <span class="icon fui-gear"> </span>
                            <a class="fui-arrow-right pt-control-next" href="#"> </a>
                        </div>
                        <div class="row">
                            <div class="col-sm-6 col-sm-offset-3">
                                <h3>Our Mission</h3>

                                <div class="article-info">
                                    <span><span class="fui-user"> </span> CHRIS MARTIN</span>
                                    <span><span class="fui-time"> </span> 10 MAY</span>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-8 col-sm-offset-2">
                                <p style="margin: 0">
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ac tincidunt arcu. Maecenas vel tellus ut magna bibendum elementum. Donec suscipit pharetra ligula id consectetur. Sed id erat orci. Donec nec metus imperdiet tortor pulvinar mattis. Proin ut erat ac est ultrices feugiat. Integer hendrerit ullamcorper tellus, at tempor odio tristique vitae. Curabitur tincidunt risus justo, tristique fermentum quam molestie non. Cras bibendum eget quam quis congue. In suscipit mollis magna id tincidunt. Curabitur sit amet ligula vitae libero auctor ultrices. Nam vitae tortor tristique, tempus nulla ultricies, malesuada augue. Quisque convallis tristique sem, et volutpat enim tempus sed. Ut lobortis pellentesque neque ac feugiat.
                                    <br><br>
                                    Aenean et suscipit ante. Integer malesuada tempus vestibulum. Nulla posuere adipiscing lectus vitae tristique. Proin venenatis sodales laoreet. Nam dictum leo ac nibh porta, vestibulum sollicitudin risus lacinia. Integer ac porta risus, ac feugiat orci. Aliquam malesuada dolor non laoreet convallis. Duis mauris massa, tincidunt et volutpat nec, posuere et ante. Vivamus pulvinar ante vel augue pellentesque sodales. Vestibulum molestie euismod ultrices. Pellentesque nunc diam, commodo sed ligula ultricies, dapibus hendrerit massa. Nam varius tortor tortor, rutrum consequat nibh feugiat eget. Donec aliquet interdum nisl eget vulputate.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        """

        adaythere.open_element("section", {"id":"about", "class":"about-sections"})\
            .append_to_element(about_display)\
            .close_element("section")

        contact_display = """
            <div class="container">
                <div class="row">
                    <div class="col-sm-5">
                        <h3>Get in touch with us</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                        <div class="links">
                            <a href="#"><span class="fui-phone"></span> +1 250 555 5555</a>
                            <br>
                            <a href="#"><span class="fui-mail"></span> info@adaythere.com</a>
                        </div>
                        <h6>Where to find us</h6>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                        <div class="map">
                            <!--map-->
                            <iframe width="100%" height="100%" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/?ie=UTF8&amp;t=m&amp;ll=48.4230037,-123.3692806&amp;spn=0.04554,0.072956&amp;z=12&amp;output=embed"></iframe>
                        </div>
                    </div>
                    <div class="col-sm-6 col-sm-offset-1">
                        <h3>You can mail us</h3>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                        <form>
                            <label class="h6">Name / Last Name</label>
                            <input type="text" class="form-control">
                            <label class="h6">E-mail</label>
                            <input type="text" class="form-control">
                            <label class="h6">Message</label>
                            <textarea rows="7" class="form-control"></textarea>
                            <button type="submit" class="btn btn-primary"><span class="fui-mail"></span>
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        """

        adaythere.open_element("section", {"id":"contact", "class":"contacts"})\
            .append_to_element(contact_display)\
            .close_element("section")

        footer_display = """
            <div class="container">
                <a href="#"><span class="fui-home"> </span></a>
                <nav>
                    <ul>
                        <li><a href="#about">ABOUT US</a></li>
                        <li><a href="#day_search">FIND A DAY</a></li>
                        <li class="scroll-btn"><a href="#" class="scroll-top fui-arrow-up"> </a></li>
                        <li><a href="/tools">CREATE A DAY</a></li>
                        <li><a href="#contact">CONTACT</a></li>
                    </ul>
                </nav>
                <div class="social-btns">
                    <a href="#">
                        <div class="fui-facebook"></div>
                        <div class="fui-facebook"></div>
                    </a>
                    <a href="#">
                        <div class="fui-twitter"></div>
                        <div class="fui-twitter"></div>
                    </a>
                </div>
            </div>
        """

        adaythere.open_element("footer", {"id":"page_footer", "class":"footer"})\
            .append_to_element(footer_display)\
            .close_element("footer")

        adaythere.close_element("div")

        self.response.write(adaythere.get())

class MapTools():

    @classmethod
    def map_elements (cls):
        logged_in = True
        element = Elements ()
        element.open_element("section", {"id":"map_section"})\
            .close_element("section")

        sidebarHeaderView = SidebarHeaderView()
        mapSearchView = MapSearchView(logged_in)
        placesSearchView = PlacesSearchView(logged_in)
        markersView = MarkersView(logged_in)
        createADayView = CreateADayView(logged_in)
        myDaysView = MyDaysView(logged_in)

        profileModal = ProfileModal()
        markerModal = MarkerModal()
        selectDayModal = SelectDayModal()
        addPhotosModal = AddPhotosModal()

        element.open_element("section", {"id":"sidebar_section", "ng-controller":"sidebarCtrl"})\
            .open_element("header", {"id":"sidebar_heading"})\
            .append_to_element(sidebarHeaderView.get())\
            .close_element("header")\
            .append_to_element("<hr></hr>")\
            .open_element("tabset", {"justified":"false"})\
            .open_element("tab", {"heading":"Map Tools"})\
            .open_element("accordion", {"close-others":"true"})\
            .open_element("accordion-group",{"heading":"Location"})\
            .append_to_element(mapSearchView.get())\
            .close_element("accordion-group")\
            .open_element("accordion-group", {"heading":"Places"})\
            .append_to_element(placesSearchView.get())\
            .close_element("accordion-group")\
            .open_element("accordion-group", {"heading":"Markers"})\
            .append_to_element(markersView.get())\
            .close_element("accordion-group")\
            .close_element("accordion")\
            .close_element("tab")\
            .open_element("tab", {"heading":"Create Day"})\
            .append_to_element(createADayView.get())\
            .close_element("tab")\
            .open_element("tab", {"active":"find_a_day.active", "heading":"My Days"})\
            .append_to_element(myDaysView.get())\
            .close_element("tab")\
            .close_element("tabset")\
            .open_element("div", {"ng-controller":"profileCtrl"})\
            .append_to_element(profileModal.get())\
            .close_element("div")\
            .open_element("div")\
            .append_to_element(markerModal.get())\
            .close_element("div")\
            .open_element("div")\
            .append_to_element(selectDayModal.get())\
            .close_element("div")\
            .open_element("div")\
            .append_to_element(addPhotosModal.get())\
            .close_element("div")\
            .close_element("section")
        return element



app = webapp2.WSGIApplication([
    ('/', ToolsHandler),
    ('/tools', ToolsHandler),
    ('/home', HomeHandler),
    ('/photos', app.photos.PhotosHandler),
    ('/days', app.days.DayHandler),
    ('/login', app.login.LoginHandler),
    ('/logout', app.login.LogoutHandler),
    ('/profile', app.profile.ProfileHandler),
    ('/admin_profiles', app.admin.ProfilesHandler),
    ('/keywords', app.keywords.KeywordHandler),
    ('/locality_days', app.locality_days.LocalityDaysHandler)
], debug=True)

