
from webapp2_extras import i18n
import re

class LoggedInNavView:

    def __init__(self, db_user):
        admin_menu = ""

        if re.match (".*@adaythere.com?", db_user.email):
            admin_menu = """
                <li class="dropdown" ng-controller="adminCtrl">
                    <a href class="dropdown-toggle">
                        Admin
                    </a>
                    <ul class="dropdown-menu adt-nav-menu-button">
                        <a ng-click="admin_profiles()">profiles</a>
                    </ul>
                </li>
            <li id="sidebar_display_menu_item" ng-controller="sidebarDisplayCtrl" style="list-style:none; position:absolute; right:10px; top:5px">
                <a href ng-click="toggle_sidebar ()">
                    {{ sidebar_display.menu_text }}
                </a>
            </li>
            """

        self.html = """
            <li class="dropdown" ng-controller="loginCtrl">
                <a href class="dropdown-toggle">
                    Logout
                </a>
                <ul class="dropdown-menu adt-nav-menu-button">
                    <a ng-click="googlelogout()">Google Logout</a>
                </ul>
            </li>
            <li class="dropdown" ng-controller="profileCtrl">
                <a href class="dropdown-toggle">
                    {0}
                </a>
                <ul class="dropdown-menu adt-nav-menu-button">
                    <a ng-click="profile()">Profile</a>
                </ul>
            </li>
            {1}
        """.format(db_user.name, admin_menu)


    def get(self):
        return self.html



