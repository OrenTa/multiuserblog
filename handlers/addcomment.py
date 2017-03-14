from handler import Handler
from models import User, Post, Comment

from google.appengine.ext import db

class AddComment(Handler):
    def post(self):
        user = self.request.cookies.get('user',-1)
        if user==(-1): 
            self.redirect("/message/1")
        else: 
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):
                dbpost = Post.get_by_id(int(self.request.get('postid')))
                if dbpost:
                    comment = self.request.get('comment')
                    c = Comment(user=dbuser, post=dbpost, content=comment)
                    c.put()
                    self.redirect("/"+str(dbpost.key().id()))
                else:
                    self.redirect("/message/9") # a "something went wrong" message
            else:
                self.redirect("/message/1")
