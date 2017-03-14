# NewPost handler for creating new posts in the DB.
# **************

from handler import Handler
from check import Check
from models import User, Post
import hmac
import sys
from google.appengine.ext import db

class NewPost(Handler):
    """adding a new post to the blog"""
    def get(self):
        user = self.request.cookies.get('user',-1)
        # if there's no cookie
        if user==(-1):
            self.redirect("/login")
        else:
            # check that the cookie is valid
            print "NewPost get called"
            sys.stdout.flush()
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):
                if self.request.get('postid'):
                    content = self.request.get('content')
                    subject = self.request.get('subject')
                    postid = self.request.get('postid')
                    self.render("addpost.html", logstatus="Signed in as " + dbuser.Name, title="edit post",
                                subject=subject, content=content, postid=postid)
                else:
                    self.render("addpost.html", logstatus="Signed in as " + dbuser.Name, title="add new post")
            else:
                self.redirect("/login")

    def post(self):
        subject_ = self.request.get('subject')
        content_ = self.request.get('content')
        user = self.request.cookies.get('user',-1)
        postid_= self.request.get('postid')
        action = self.request.get('btn')
        if action =='cancel':
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
                    # now it checks if we're in a new blog post or editing an existing post.
                    if postid_=="": #this is a new post
                        # print "Inside Post of Newpost - recognized it's a new post"
                        # sys.stdout.flush()
                        if content_ and subject_:
                            p = Post(subject=subject_, content=content_, user=dbuser)
                            b_key = p.put()
                            self.redirect("/%d" % b_key.id())
                        else:
                            self.render("addpost.html", subject=subject_, content=content_, error="something is missing",
                                        title="add new post")
                    else:# as postid_ is not empty editing existing post.                 
                        dbpost = Post.get_by_id(int(postid_))
                        if dbpost:
                            dbpost.subject = subject_
                            dbpost.content = content_
                            dbpost.put()
                            self.redirect("/")
                        else:
                            self.redirect("/message/9")
                # cookie is not valid
                else:
                    self.redirect("/message/4")
