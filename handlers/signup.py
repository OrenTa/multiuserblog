from handler import Handler
from check import Check
from config import * #this file includes the key
from models import User
import hmac

class Signup(Handler):
    def get(self):
        user = self.request.cookies.get('user',-1)
        if user==(-1):
            #it means there's no cookie - redirecting to signup
            self.render("signup.html",logstatus="Not signed in")
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):       
                self.render("signup.html", logstatus="Signed in as " + dbuser.Name)
            else:
                self.render("signup.html")

    def post(self):
        username_ = self.request.get('username')
        password_ = self.request.get('password')
        verify_ = self.request.get('verify')
        email_ = self.request.get('email')
        if not email_:
            email_=""          
        result = Check(username_, password_, verify_, email_)
        if result[8]:         
            hpassword = hmac.new(key,password_).hexdigest()
            u = User(Name=username_, HashedPassword=hpassword, Email=email_)
            uid = u.put()
            self.response.headers.add_header('Set-Cookie', "user=%s|%s" % (uid.id(),hpassword))
            self.redirect("/welcome")
        else:
            self.render("signup.html", username=result[0], user_error=result[1],
                        password=result[2], pswd_error=result[3],
                        verify=result[4], verify_error=result[5],
                        email=result[6], email_error=result[7],
                        check=result[8])

