# Signin Handler
# **************

from handler import Handler
from check import Check
from config import * #this file includes the key
from models import User
import hmac

from google.appengine.ext import db

class Signin(Handler):
    def get(self):
        user = self.request.cookies.get('user',-1)
        # if there's no cookie
        if user==(-1):
            self.render("signin.html", username="", password="", logstatus="Not signed in")
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):
                self.redirect("/welcome")
            else:
                self.render("signin.html", username="", password="", logstatus="Not signed in")    
            

    def post(self):
        username_ = self.request.get('username')
        password_ = self.request.get('password')
        
        result = Check(username_, password_, password_, "oren@oren.com", False)
        if result[8]:         
            dbuser = db.GqlQuery("SELECT * FROM User WHERE Name = :n", n=username_)
            if dbuser.count() > 0 and dbuser.get().HashedPassword == hmac.new(key,password_).hexdigest():
                hpassword = hmac.new(key,password_).hexdigest()
                self.response.headers.add_header('Set-Cookie', "user=%s|%s" % (dbuser.get().key().id(),hpassword))
                self.redirect("/welcome")
            else:
                self.render("signin.html", username="", user_error="user doesn't exist or password doesn't match[1]",
                            password="", pswd_error="")
                    
        else:
            self.render("signin.html", username="", user_error="user don't exist or password don't match[2]",
                        password="", pswd_error="")
