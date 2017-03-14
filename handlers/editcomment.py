# edit comment handler

from handler import Handler
from models import User, Comment
from google.appengine.ext import db


class EditComment(Handler):
    def get(self, commentid):
        user = self.request.cookies.get('user',-1)
        if user==(-1):
           self.render("signin.html", username="", password="", logstatus="Not signed in", title="sign in")
        else:
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            commentid_=int(commentid)
            dbcomment = Comment.get_by_id(commentid_)
            if dbcomment and dbuser:
                if dbuser.key() == dbcomment.user.key():
                    self.render("editcomment.html", title ="edit post", comment=dbcomment)
                else:
                    self.redirect("/message/3")
            else:
                self.redirect("/message/9")

    def post(self, commentid):
        comment_ = self.request.get('comment')
        commentid_= self.request.get('commentid')
        action = self.request.get('btn')
        user = self.request.cookies.get('user',-1)
        if action == 'cancel':
            self.redirect("/")
        else:
            # if there's no cookie
            if user==(-1):
                self.render("signin.html", username="", password="", logstatus="Not signed in", title="add new post")
            else:
                # check that the cookie is valid
                (cookie_uid,cookie_hash) = user.split("|")
                dbuser = User.get_by_id(int(cookie_uid))
                if dbuser and (dbuser.HashedPassword==cookie_hash):
                    dbcomment = Comment.get_by_id(int(commentid_))
                    if dbcomment:
                        if dbuser.key() == dbcomment.user.key(): 
                            dbcomment.content = comment_
                            dbcomment.put()
                            self.redirect("/")
                        else:
                            self.redirect("/message/3")
                    else:
                        self.redirect("/message/9")
                # cookie is not valid
                else:
                    self.redirect("/message/4")
