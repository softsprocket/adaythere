"""
    Web models and views for Twitter places 
"""

from app.lib.twitter.useroauth import UserOAuth
from app.lib.twitter.connection import Connection
from app.lib.db.twitterplaces import PlacesQuery
from google.appengine.api import memcache
import logging
import urllib
import hashlib

class QueryModel:

    memcache_key = "Twitter.Query."

    def __init__(self, place):
        self.place = place
        self.place_key = hashlib.md5(place).hexdigest()

    def __getFromTwitter(self):

        oauth = UserOAuth("adaythere")
        conn = Connection(oauth)

        res = conn.get("/1.1/geo/search.json?query=" + urllib.quote(self.place))

        return (res.status == 200, res.read())


    def get(self):

        status = False
        data = "{}"
        
        logging.info("Memcache.get(%s)", self.memcache_key + self.place_key)
        query = memcache.get(self.memcache_key + self.place_key)

        if query is None:
            logging.info("getFromTwitter()")
            status, data  = self.__getFromTwitter()
            if status:
                memcache.add(self.memcache_key + self.place, data)
        else:
            data = query
            status = True

        logging.info("%s, %s", status, data);
        return (status, data)


class QueryView:

    def __init__(self):
        self.html = """
            <div ng-controller="twitterQueryCtrl">
                <input ng-model="place">
                <button ng-click="setPlace(place)">Query</button>
                <ul>
                    <li ng-repeat="p in places">
                        {{p}}
                    </li>
               </ul>
            </div>
        """


    def get(self):
        return self.html


class IPModel:
    
    def __init__(self, ipaddr):
        self.ipaddr = ipaddr

    def get(self):
        
        oauth = UserOAuth("adaythere")
        conn = Connection(oauth)

        res = conn.get("/1.1/geo/search.json?ip=" + self.ipaddr)

        return (res.status == 200, res.read())


class IPView:

    def __init__(self):
        
        self.html = """
            <div ng-controller="TwitterIPCtrl">
                {{place}}
            </div>
        """


    def get(self):

        return self.html


