"""
    Top level class for the website. It generates the main page for adaythere.com
"""
from app.lib.components.document import Html5Document

class ADayThere(Html5Document):

    def __init__(self):
        """
            Constructor. Initializes html document.
        """
        
        Html5Document.__init__(self, "A Day There", {"ng-app":"adaythere"})




