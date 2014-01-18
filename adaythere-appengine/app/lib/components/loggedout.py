
from webapp2_extras import i18n

class LoggedOutNavModel:

    def __init__(self):
        None

    def get(self):
        return ""


class LoggedOutNavView:

    def __init__(self):

        menuitems = [
            { 
                'function': 'userlogin(user)',
                'text': i18n.gettext('login')
            }
        ]

        self.html = """
                <ul ng-controller="menuCtrl">"""
                                                                                 
        for item in menuitems:
            self.html += '<li><a href="#" ng-click="{0}">{1}</a></li>'.format(item['function'], item['text'])                                                                          
                                                                                                                 
        self.html += """            
                </ul>"""

    def get(self):
        return self.html


