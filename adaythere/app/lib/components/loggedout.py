
from webapp2_extras import i18n


class LoggedOutNavView:

    def __init__(self):

        self.html = """
        <ul class="page-header-nav">
            <li class="dropdown" ng-controller="loginCtrl" style="list-style:none">
                <a href class="dropdown-toggle">
                    Login
                </a>
                <ul class="dropdown-menu adt-nav-menu-button">
                        <a ng-click="googlelogin()">Google Login</a>
                </ul>
            </li>
        </ul>
        """


    def get(self):
        return self.html


