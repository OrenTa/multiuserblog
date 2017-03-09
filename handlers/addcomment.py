from handler import Handler
from check import Check
from config import * #this file includes the key
from models import User, Post, Comment
import hmac

from google.appengine.ext import db

class AddComment(Handler):
    def post(self):
        user = self.request.cookies.get('user',-1)     
        (cookie_uid,cookie_hash) = user.split("|")
        dbuser = User.get_by_id(int(cookie_uid))
        dbpost = Post.get_by_id(int(self.request.get('postid')))
        comment = self.request.get('comment')
        c = Comment(user=dbuser, post=dbpost, content=comment)
        c.put()
        self.redirect("/"+str(dbpost.key().id()))
