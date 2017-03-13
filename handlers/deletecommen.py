from handler import Handler
from models import User, Comment

from google.appengine.ext import db

class DeleteComment(Handler):
    def post(self):
        user = self.request.cookies.get('user',-1)
        # if there's no cookie
        if user==(-1):
            self.render("signin.html", username="", password="", logstatus="Not signed in", title="sign in")
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash): # cookie is valid
                commentid_=self.request.get('commentid')
                dbcomment = Comment.get_by_id(int(commentid_))
                if dbcomment.user.key()==dbuser.key(): #verify the user is trying to delete his own comment
                    dbcomment.delete()
                    self.redirect("/")
                else: #this is not his own comment
                    self.redirect("/message/8")
                    
            else: # cookie is not valid
                self.redirect("/message/4")
