import httplib
from urlparse import urlparse, parse_qsl
from useroauth import UserOAuth
from appoauth import AppOAuth

class ConnectionException(httplib.HTTPException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Connection:

    host = "api.twitter.com"

    def __init__(self, oauth):
        """ initializes a connection with an oauth object  
        """

        self.oauth = oauth
        self.conn = httplib.HTTPSConnection(Connection.host)
        self.headers = {}

    
    def add_header(self, k, v):
        self.headers[k] = v

    def __setapp_auth(self) :
        self.add_header("Authorization", self.oauth.get_token(self.conn))
        self.add_header("User-Agent", self.oauth.useragent())   
        
    def __setuser_auth(self, method, path, body):

        p = urlparse(path)
        path = p.path
        query = parse_qsl(p.query)
    
        if body is not None:
            query = parse_qsl(body) + query
             
        oauth_token = self.oauth.get_token(method, "https://{0}{1}".format(Connection.host, path), query)

        self.add_header("Authorization", oauth_token)
        self.add_header("User-Agent", self.oauth.useragent())   
        

    def get(self, path):
        """ GET from twitter api
        """
    
        if type(self.oauth) is AppOAuth:
            self.__setapp_auth()
        elif type(self.oauth) is UserOAuth:
            self.__setuser_auth('GET', path, None)

        self.conn.request("GET", path, None, self.headers)
 
        return self.conn.getresponse()


    def post(self, path, body):
        """ POST to twitter api
        """

        if type(self.oauth) is AppOAuth:
            self.__setapp_auth()
        elif type(self.oauth) is UserOAuth:
            self.__setuser_auth("POST", path, body)


