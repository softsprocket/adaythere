
from useroauth import UserOAuth
from connection import Connection

oauth = UserOAuth("adaythere")
conn = Connection(oauth)

res = conn.get("/1.1/geo/search.json?query=Victoria")

print res.status
print res.read()


