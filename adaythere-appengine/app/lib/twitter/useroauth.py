import urllib
import string
import random
import time
import hashlib 
import hmac

class UserOAuth(object):

    apps = {
        "test": {
            "agent": "test",
            "consumer_key": "xvz1evFS4wEEPTGEFPHBog",
            "consumer_secret": "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw",
            "access_token": "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb",
            "access_token_secret": "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE"

        },
        "adaythere": {
            "agent": "A Day There",
            "consumer_key": "5pyEYqQqq81RtzONCWOasg",
            "consumer_secret": "sV2zjOwDGgy7ME2TKNwwScRBHHzhvl13aNtqnqTXz8",
            "access_token": "1961581322-JnH7F1R2ObTwOAVbwVkijLwSXNJoBn7YOyPcXTq",
            "access_token_secret": "hYizkifrXVi2MS0zyN2hjGNzbqrQlh2lK0tm32thjvc"
        }
    }

    def __init__(self, app):
        self.app = UserOAuth.apps[app]


    def __nonce(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(32))

    def __signing_str(self, method, baseurl, params):
        quoted_params = sorted([(urllib.quote(k, "-._~"), urllib.quote(v, "-._~")) for k, v in params.iteritems()])     
        param_str = "&".join([x+"="+y for x , y in quoted_params])
        return "&".join([urllib.quote(method, "-._~"), urllib.quote(baseurl, "-._~"), urllib.quote(param_str, "-._~")])

    def __signing_key(self):
        return "&".join([urllib.quote(self.app["consumer_secret"], "-._~"), urllib.quote(self.app["access_token_secret"], "-._~")])

    def __signature(self, signing_key, signing_str):
        return hmac.new(signing_key, signing_str, hashlib.sha1).digest().encode("base64").strip()
        
    def get_token(self, method, url, query_params):

        params = {
            "oauth_consumer_key": self.app["consumer_key"],
            "oauth_nonce": self.__nonce(),
            "oauth_token": self.app["access_token"],
            "oauth_timestamp": str(int(time.time())),
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_version":  "1.0"
        }

        if self.app["agent"] == "test" :
            params["oauth_nonce"] = "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg";
            params["oauth_timestamp"] = str(1318622958);

        secret_params = {}
        secret_params.update(params)
        secret_params.update(query_params);
        
        signing_str = self.__signing_str(method, url, secret_params);
        signing_key = self.__signing_key();
        signature = self.__signature(signing_key, signing_str);
        params["oauth_signature"] = signature

        quoted_params = {k: urllib.quote(v, "-._~") for k, v in params.iteritems()}
        dst = []
        for k, v in quoted_params.iteritems():
            dst.append("{0}=\"{1}\"".format(k, v))
        
        dst_str = ", ".join(dst)  

        return "OAuth {0}".format(dst_str)


    def useragent(self):
        return self.app["agent"]


