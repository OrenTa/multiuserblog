# This handler deals with the edit button and logic
# the main page is rendered in a way that this class will only be called when
# a user is logged in. So we only need to check that the post belongs to the user.
# if the post belongs to the user - we render the add post page with the existing text (to enable modify)
# otherwise we generate an erro saying you can only edit your own posts (2).

from handler import Handler
from models import User, Post
from google.appengine.ext import db


class EditPost(Handler):
    def get(self):
        user = self.request.cookies.get('user',-1)
        if user==(-1):
           self.render("signin.html", username="", password="", logstatus="Not signed in", title="sign in")
        else:
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            postid_=self.request.get('postid')
            dbpost = Post.get_by_id(int(postid_))
            if dbpost and dbuser:
                if dbuser.key() == dbpost.user.key():
                    self.render("editpost.html", title ="edit post", post=dbpost, postid=postid_)
                else:
                    self.redirect("/message/3")
            else:
                self.redirect("/message/9")

    def post(self):
        subject_ = self.request.get('subject')
        content_ = self.request.get('content')
        postid_= self.request.get('postid')
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
                    dbpost = Post.get_by_id(int(postid_))
                    if dbpost:
                        if dbuser.key() == dbpost.user.key(): 
                            dbpost.subject = subject_
                            dbpost.content = content_
                            dbpost.put()
                            self.redirect("/")
                        else:
                            self.redirect("/message/3")
                    else:
                        self.redirect("/message/9")
                # cookie is not valid
                else:
                    self.redirect("/message/4")
