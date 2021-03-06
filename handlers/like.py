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
            self.redirect("/message/10") #message requiring to be siged-in to like  
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash): #it means there's a validated user
                # dbpost = Post.get_by_id(int(self.request.get('postid')))
                key = db.Key.from_path('Post', int(self.request.get('postid')))
                dbpost = db.get(key)
                if not dbpost:
                    return self.redirect('login')
                else:
                    existing_likes = db.GqlQuery("SELECT * FROM Likes WHERE user = :n AND post = :m ", n=dbuser, m=dbpost)
                    #check if the user is trying to like his own post
                    if dbuser.key()==dbpost.user.key(): 
                        self.redirect("/message/6")
                    else:
                        if existing_likes.count()==0:
                            #create a new line in the likes table
                            l = Likes(user=dbuser, post=dbpost)
                            l.put()
                            self.redirect("/")
                        else: #otherwise - the like is removed 
                            for li in existing_likes:
                                li.delete()
                            self.redirect("/")
            else:
                self.redirect("/message/10") #message requiring to be siged-in to like
