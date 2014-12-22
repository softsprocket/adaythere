
from webapp2_extras import i18n
import re
from app.adaythere import ADayThere

def get_help_menu ():
    return """
            <li class="dropdown" ng-controller="loginCtrl" style="list-style:none">
                <a href ng-click="open_help ()">
                    Help
                </a>
            </li>
    """

class LoggedInNavView:

    def __init__(self, db_user):
        admin_menu = ""

        tool_user, holder = ADayThere.tool_user ()
        
        if ADayThere.admin_user (db_user):
            admin_menu = """
                <li class="dropdown" ng-controller="adminCtrl">
                    <a href="/admin" class="dropdown-toggle">
                        Admin
                    </a>
                    <ul class="dropdown-menu adt-nav-menu-button">
                        <a href="/admin?type=profiles">profiles</a>
                        <a href="/admin?type=days">days</a>
                    </ul>
                </li>
            """
        

        self.html = """
            <li class="dropdown" ng-controller="loginCtrl">
                <a href ng-click="googlelogout()" class="dropdown-toggle">
                    Logout
                </a>
            </li>
            <li class="dropdown" ng-controller="profileCtrl">
                <a href class="dropdown-toggle" id="profile_ctrl_menu_toggle">
                    {0}
                </a>
                <ul id="tool_user_related_menu" class="dropdown-menu adt-nav-menu-button">
        """.format(db_user.name)

        if tool_user:
            self.html +=  LoggedInNavView.tool_user_menus ()
        else:
            self.html += LoggedInNavView.non_tool_user_menus ()

        self.html += """
                </ul>
                {0}
            </li>
            <a href popover-placement="bottom" popover-trigger="mouseenter" popover="Click links to see drop down menus">?</a>
            {1}
        """.format(get_help_menu (), admin_menu)

    
    @classmethod
    def tool_user_menus (cls):
        return """
            <a ng-click="profile()">Profile</a>
            <a ng-click="gotoToolsPage()">Go to Tools</a>
            <a ng-click="gotoSearchPage()">Go to Search</a>
        """        

    @classmethod
    def non_tool_user_menus (cls):
        return  """
            <a ng-click="become_a_contributor()">Go to Tools</a>
            <a ng-click="gotoSearchPage()">Go to Search</a>
        """


    def get(self):
        return self.html



