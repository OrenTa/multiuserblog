# This class is used to present error messages to the user
# To call it you need to call /message/# where # represents the number of the error message
# Then the class renders the message page (message.html) with the appropriate error message

from handler import Handler

class Message(Handler):
    def get(self,id):
        if id=="1":
            m = "You need to be signed-in to comment or delete a post.(g)"
        elif id=="2":
            m = "You need to be signed-in to edit your posts. (g)" 
        elif id=="3":
            m = "You can not edit posts of other users. You can however edit your own posts ! (g)"
        elif id=="4":
            m = "There's some error with your cookie. please logout and sign in again (g)"
        elif id=="5":
            m = "You need to be signed-in to delete a post. (g)"
        elif id=="6":
            m = "You can only like posts of other users. (g)"
        elif id=="7":
            m = "You are now logged out. (g)"
        elif id=="8":
            m = "You can only delete your own posts and comments. (g)"
        elif id=="9":
            m = "Something went wrong. (g)"
        elif id=="10":
            m = "You need to be logged-in to like a post. (g)"
        self.render("message.html",message=m)

    def post(self,id):
        if id=="1":
            m = "You need to be signed-in to comment or delete a post.(p)"
        elif id=="2":
            m = "You need to be signed-in to edit your posts.(p)" 
        elif id=="3":
            m = "You can not edit posts of other users. You can however edit your own posts !(p)"
        elif id=="4":
            m = "There's some error with your cookie. please logout and sign in again (p)"
        elif id=="5":
            m = "You need to be signed-in to delete a post. (p)"
        elif id=="6":
            m = "You can only like posts of other users. (p)"
        elif id=="7":
            m = "You are now logged out. (p)"
        elif id=="8":
            m = "You can only delete your own posts and comments. (p)"
        elif id=="9":
            m = "Something went wrong. (p)"
        elif id=="10":
            m = "You need to be logged-in to like a post. (p)"
        self.render("message.html",message=m)

