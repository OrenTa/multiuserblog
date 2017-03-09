from handler import Handler
from models import User

class Welcome(Handler):
    def get(self):
        user = self.request.cookies.get('user',-1)
        if user==(-1):
            #it means there's no cookie - redirecting to signup
            self.redirect("/signup")
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):       
                self.render("welcome.html", username=dbuser.Name, logstatus="Signed in as " + dbuser.Name)
            else:
                self.redirect("/signin")
