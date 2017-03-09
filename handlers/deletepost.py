from handler import Handler
from check import Check
from config import * #this file includes the key
from models import User, Post
import hmac

from google.appengine.ext import db

class DeletePost(Handler):
    def get(self):
        user = self.request.cookies.get('user',-1)     
        (cookie_uid,cookie_hash) = user.split("|")
        dbuser = User.get_by_id(int(cookie_uid))
        postid_=self.request.get('postid')
        dbpost = Post.get_by_id(int(postid_))
        if dbuser.key() == dbpost.user.key():
            self.render("deletepost.html", post_title=dbpost.subject, postid=postid_)
        else:
            self.redirect("/message/8")

    def post(self):
        postid_= self.request.get('postid')
        user = self.request.cookies.get('user',-1)
        # if there's no cookie
        if user==(-1):
            self.render("signin.html", username="", password="", logstatus="Not signed in", title="add new post")
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):
                dbpost = Post.get_by_id(int(postid_))
                dbpost.delete()
                self.redirect("/")
            # cookie is not valid
            else:
                self.redirect("/message/4")
