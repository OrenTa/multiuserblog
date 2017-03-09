# Add http://webapp2.readthedocs.io/en/latest/guide/exceptions.html 404 and 500

import os
import webapp2
import jinja2
import re
import hmac
import pdb
import sys
from google.appengine.ext import db

from models import User, Comment, Likes, Post
from handlers import Signup, Check, Handler, Signin, Signout, DeletePost
from handlers import EditPost, NewPost, DeletePost, AddComment, Like, Welcome
from handlers import Permalink, MyPosts, Message
from handlers.config import *
          
class Main(Handler):
    def get(self):
        log_stat=""
        user = self.request.cookies.get('user',-1)
        # if there's no cookie
        if user==(-1):     
            log_stat="Not signed in"
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):       
                log_stat="Signed in as " + dbuser.Name
            else:
                log_stat="Not signed in"
        posts_ = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        if log_stat=="Not signed in":
            comment_url="message/1"
            edit_url = "message/2"
            delete_url="message/5"
        else:
            comment_url="comment"
            edit_url="editpost"
            delete_url="deletepost"
        self.render("main.html", logstatus=log_stat, posts=posts_, comment_url=comment_url, edit_url=edit_url,
                    delete_url=delete_url)
                
         

app = webapp2.WSGIApplication([('/', Main),('/signup', Signup), ('/welcome', Welcome),
                               ('/login', Signin), ('/logout',Signout),
                               ('/newpost', NewPost), (r'/(\d+)', Permalink),('/like', Like),
                               ('/myposts', MyPosts),('/comment', AddComment),
                               (r'/message/(\d+)', Message), ('/editpost', EditPost),
                               ('/deletepost', DeletePost)], debug=True)
