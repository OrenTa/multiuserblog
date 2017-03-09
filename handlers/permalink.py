# implements the Permalink handler
# this is called to render a page of a single post
# triggered ususally automatically after post creation
# ****************************************************

from handler import Handler
from models import User, Post
from google.appengine.ext import db

class Permalink(Handler):
    def get(self, blog_id):
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
        post = Post.get_by_id(int(blog_id))
        comments_of_post = db.GqlQuery("SELECT * FROM Comment WHERE post =:m", m=post)
        self.render("lastpost.html", post=post, logstatus=log_stat, comments=comments_of_post)            

