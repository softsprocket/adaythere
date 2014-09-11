from google.appengine.ext import ndb

class UserComment (ndb.Model):

    userid = ndb.StringProperty () 
    title = ndb.StringProperty ()
    rating = ndb.IntegerProperty () 
    text = ndb.StringProperty ()
    commenters_id = ndb.StringProperty ()

    @classmethod
    def query_comments (cls, userid, title):
        return cls.query (cls.userid == userid, cls.title == title)

    
    @classmethod
    def query_previous_comment (cls, commenters_id, userid, title):
        return cls.query (cls.commenters_id == commenters_id, cls.userid == userid, cls.title == title)


