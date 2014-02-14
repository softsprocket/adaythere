
from webapp2_extras import i18n


class LoggedInNavView:

    def __init__(self, db_user):

        self.html = """
            <li class="dropdown" ng-controller="loginCtrl">
                <a href class="dropdown-toggle">
                    logout
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
        """.format(db_user.name)


    def get(self):
        return self.html



