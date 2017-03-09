# This handler deals with the like button and logic

from handler import Handler
from check import Check
from models import User, Likes, Post 
import hmac

from google.appengine.ext import db

class Like(Handler):
    def post(self):
        log_stat=""
        check_own=""
        user = self.request.cookies.get('user',-1)
        # if there's no cookie so no like is possible
        if user==(-1):     
            log_stat="Not signed in"     
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash): #it means there's a validated user       
                log_stat="Signed in as " + dbuser.Name
                dbpost = Post.get_by_id(int(self.request.get('postid')))
                existing_likes = db.GqlQuery("SELECT * FROM Likes WHERE user = :n AND post = :m ", n=dbuser, m=dbpost)
                #check if the user is trying to like his own post
                if dbuser.key()==dbpost.user.key(): 
                    check_own="own"
                else:
                    if existing_likes.count()==0:
                        #create a new line in the likes table
                        l = Likes(user=dbuser, post=dbpost)
                        l.put()
                    else: #otherwise - the like is removed or the user is not allowed to like his own
                        for li in existing_likes:
                            li.delete()                  
            else:
                log_stat="Not signed in"

        if check_own=="own":
            self.redirect("/message/6")
        else:
            self.redirect("/")
