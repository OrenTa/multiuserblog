# implements the handler for presenting myposts
# *********************************************

from handler import Handler
from models import User, Post
from google.appengine.ext import db

class MyPosts(Handler):
    def get(self):
        log_stat=""
        user = self.request.cookies.get('user',-1)
        # if there's no cookie then no like is done...
        if user==(-1):     
            log_stat="Not signed in"
            posts_ = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC ")        
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):       
                log_stat="Signed in as " + dbuser.Name
                posts_ = db.GqlQuery("SELECT * FROM Post WHERE user = :n ORDER BY created DESC ", n=dbuser)
            else:
                log_stat="Not signed in"
                posts_ = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC ")        

        self.render("myposts.html", logstatus=log_stat, posts=posts_)
