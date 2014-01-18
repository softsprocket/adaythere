from useroauth import UserOAuth
from connection import Connection

oauth = UserOAuth("test")
conn = Connection(oauth)


res = conn.post("/1/statuses/update.json?include_entities=true", "status=Hello%20Ladies%20%2b%20Gentlemen%2c%20a%20signed%20OAuth%20request%21")



