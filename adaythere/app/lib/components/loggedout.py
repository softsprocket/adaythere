
from webapp2_extras import i18n
from app.lib.components.loggedin import get_help_menu, get_contact_menu

class LoggedOutNavView:

    def __init__(self):

        self.html = """
        <ul class="page-header-nav">
            <li class="dropdown" ng-controller="loginCtrl" style="list-style:none">
                <a href id="user_not_logged_in" ng-click="googlelogin()"  class="dropdown-toggle">
                    Login
                </a>
            </li>
            {0}
            {1}
        </ul>
        """.format (get_help_menu (), get_contact_menu ())


    def get(self):
        return self.html


