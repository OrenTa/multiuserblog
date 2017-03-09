# Signout (logout) handler
# ************************

from handler import Handler

class Signout(Handler):
    def get(self):
        self.response.delete_cookie('user')
        self.redirect("/message/7")
