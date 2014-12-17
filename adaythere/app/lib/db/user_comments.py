from google.appengine.ext import ndb

class UserComment (ndb.Model):

    userid = ndb.StringProperty () 
    title = ndb.StringProperty ()
    rating = ndb.IntegerProperty () 
    text = ndb.StringProperty ()
    commenters_name = ndb.StringProperty ()

    @classmethod
    def query_comments (cls, userid, title):
        return cls.query (cls.userid == userid, cls.title == title)

    
    @classmethod
    def query_previous_comment (cls, commenters_name, userid, title):
        return cls.query (cls.commenters_name == commenters_name, cls.userid == userid, cls.title == title)

    @classmethod
    def query_commenter (cls, commenters_name):
        return cls.query (cls.commenters_name == commenters_name)


