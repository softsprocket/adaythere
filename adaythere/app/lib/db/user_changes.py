from app.lib.db.user_comments import UserComment
from app.lib.db.days import Day
from app.lib.db.user import User

class UserChanges ():
    def __init__ (self, userid):

        self.user = User.query_user_id (userid)


    def name (self, userid, new_name):
        
        if self.user is None:
            return (False, "User doesn't exist")

        old_name = self.user.name

        if old_name == new_name:
            return (False, "New name is same as old name")

        if User.query_name (new_name) is not None:
            return (False, "Name is already used"

        self.user.name = new_name
        self.user.put ();

        days = Day.query_user (user_id)
        if days is not None:
            all_days = days.fetch ()
            for day in all_days:
                day.name = new_name
                day.put ()

    
        comments = UserComments.query_commenter (old_name)
        if comments is not None:
            all_comments = comments.fetch ()
            for comment in all_comments:
                comment.commenters_name = new_name
                comment.put ()


        return (True, self.user)


