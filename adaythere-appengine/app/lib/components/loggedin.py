
from app.lib.components.twitterplaces import QueryView
from webapp2_extras import i18n

class LoggedInNavModel:

    def __init__(self, user):
        self.user = user

    def get(self):
        return ""


class LoggedInNavView:

    def __init__(self, user):
        self.user = user

        self.html = """
            <h1>{0}</h1>
        """.format(i18n.gettext("Logged In View"))
        

    def get(self):
        return self.html


