import webapp2
from google.appengine.api import mail
from google.appengine.api import users
import json

class SendHandler (webapp2.RequestHandler):
    def post(self):
        data = json.loads (self.request.body)

        user = users.get_current_user()
        sender = None
        if user is None:
            sender = data.get ("sender")
        else:
            sender =  user.email ()

        body = data.get ("body", '')
        name = data.get ("name")
        subject = data.get ("subject", '')

        if sender is None or not mail.is_email_valid (sender):
            self.response.status = 401 
            self.response.write ("Unauthorized")
            return

        to_addr = "info@adaythere.com"

        if not name is None:
            body = "Message from " + name + ": \n" + body


        message = mail.EmailMessage ()
        message.sender = sender
        message.subject = subject
        message.to = to_addr
        message.body = body
        message.send()


