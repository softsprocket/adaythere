import urllib
import httplib
import base64
import json

class AppOAuthException(httplib.HTTPException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AppOAuth(object):
    apps = {
        "adaythere": {
            "agent": "A Day There",
            "consumer_key": "5pyEYqQqq81RtzONCWOasg",
            "consumer_secret": "sV2zjOwDGgy7ME2TKNwwScRBHHzhvl13aNtqnqTXz8"
        }
    }

    host = "api.twitter.com"

    def __init__(self, storage, app):
        """ initialize the object with a object 
            that implements write(access_token, app)
            and read(app) which returns the access_token
            or None if it doesn"t yet exist
        """

        self.storage = storage
        self.app = app
        self.access_token = self.storage.read(app)


    def __encode_key_secret(self):
        key_secret = AppOAuth.apps[self.app]
        key = urllib.quote(key_secret["consumer_key"])
        secret = urllib.quote(key_secret["consumer_secret"])
        return base64.b64encode("{0}:{1}".format(key, secret))
        

    def get_token(self, conn):
        """ return the access_token
            if it doesn"t already exist request
            it from twitter
        """

        if self.access_token is None:
            ks = self.__encode_key_secret()    
            body = "grant_type=client_credentials"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Authorization": "Basic {0}".format(ks),
                "User Agent": AppOAuth.apps[self.app]["agent"]
            }
            
            conn.request('POST', '/oauth2/token', body, headers)
            res = conn.getresponse()
            
            resbody = res.read();

            if res.status is not 200:
                raise AppOAuthException({'status': res.status, 'body': resbody})

            authobj = json.loads(resbody)
            
            if authobj["token_type"] != "bearer":
                raise AppOAuthException({'status': res.status, 'body': resbody})

            self.access_token = authobj["access_token"]
            self.storage.write(self.access_token, self.app)
            
        return "Bearer {0}".format(self.access_token)
            
    
    def useragent(self):
        return AppOAuth.apps[self.app]["agent"]

 
