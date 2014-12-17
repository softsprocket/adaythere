import webapp2
import json
from app.lib.db.user_comments import UserComment
from app.adaythere import ADayThere
from app.lib.db.days import Day
from app.lib.db.user import User

class UserCommentsHandler (webapp2.RequestHandler):

    def put (self):
        logged_in_user, commenters_id = ADayThere.tool_user ()
       
        if not logged_in_user:
            self.response.status = 401
            return

        data = json.loads (self.request.body)

        print "DATA", data

        userid = data.get ('userid', None)
        title = data.get ('title', None)
        review = data.get ('rating', 1)

        if title is None or userid is None:
            self.response.status = 401
            return
            

        
        prev_comment = UserComment.query_previous_comment (commenters_id.name, userid, title).get ()

        if prev_comment is not None:
            self.response.status = 409
            self.response.write (json.dumps ({'rating': prev_comment.rating, 'title': prev_comment.title}))
            return

        day = Day.query_user_title (userid, title).get ()

        if day is None:
            self.response.status = 403
            return


        new_comment = UserComment ()
        new_comment.commenters_name = commenters_id.name
        new_comment.userid = userid
        new_comment.title = title
        new_comment.text = data.get ('text', None)
        new_comment.rating = review

        new_comment.put ()
        
        if day.numberOfReviews == None or day.numberOfReviews == 0:
            day.numberOfReviews = 1;
            day.averageReview = review;
        else:
            rev = (day.numberOfReviews * day.averageReview) + review
            day.numberOfReviews = day.numberOfReviews + 1
            day.averageReview = rev / day.numberOfReviews

        day.put ()

        self.response.write (json.dumps ({'numberOfReviews': day.numberOfReviews, 'averageReview': day.averageReview }));

        self.response.status = 200





    def get (self):

        userid = self.request.get ('userid', None)
        title = self.request.get ('title', None)
        limit = self.request.get ('limit', 20)
        cursor = self.request.get ('cursor', None)

        if title is None or userid is None:
            self.response.status = 401
            return

        comments_query = UserComment.query_comments (userid, title) 

        if cursor is not None:
            comments, cursor, more = comments_query.fetch_page (limit, start_cursor = cursor)
        else:
            comments, cursor, more = comments_query.fetch_page (limit)

        json_comments = []
        for each in comments:
            json_comments.append (json.dumps (each.to_dict ()))

        return_vals= {
            'comments': json_comments,
            'cursor': None,
            'more': more
        };

        if cursor is not None:
            return_vals['cursor'] = cursor.urlsafe()

        self.response.write (json.dumps (return_vals))
        self.response.status = 200


