import os
import webapp2
import jinja2
import re
import hmac
import pdb
import sys
from models import User, Comment, Likes, Post

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
#! TODOTODOTODO #!
# cosmetics !!!

key="WER#$F#sdf34!-23"

# This function checks all the inputs in the form
# It returns a list structure which include both errors (if required)
# and a final binary check True/False. True measn the form is ok.
def check(username, password, verify, email, required=True):
    # this list is used to return the results and values for showing in text boxes
    # first two items used for value of username and error text near username
    # and so on for password, verify and email
    # last item is ok/no as a binary true/false (true is ok)
    result = ["", "", "", "", "", "", "", "", "", True]
    result[8] = True

    # check username
    result[0] = username
    if not (username):
        result[1] = "Enter a user name."
        result[8] = False
    else:
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        # checking validity of user name
        if not (USER_RE.match(username)):
            result[1] = "That's not a valid user name."
            result[8] = False
        elif required:
            dbuser = db.GqlQuery("SELECT * FROM User WHERE Name = :n", n=username)
            if dbuser.count()>0:
                result[1] = "User already exists (login or select a new one)."
                result[8] = False

    # check password validity
    result[2] = ""
    USER_RE = re.compile(r"^.{3,20}$")
    # verifing there is a password and that it's ok
    if not (password) or not (USER_RE.match(password)):
        result[3] = "That's not a valid password."
        result[8] = False

    # check verify
    result[4] = ""
    if verify != password:
        result[5] = "Your passwords didn't match."
        result[8] = False

    # check email
    result[6] = email
    USER_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    if email and not (USER_RE.match(email)):
        result[7] = "Your email is not valid."
        result[8] = False

    # see above for the details of result list
    return result


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


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
        result = check(username_, password_, verify_, email_)
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
            

class Main(Handler):
    def get(self):
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
        posts_ = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        if log_stat=="Not signed in":
            comment_url="message/1"
            edit_url = "message/2"
            delete_url="message/5"
        else:
            comment_url="comment"
            edit_url="editpost"
            delete_url="deletepost"
        self.render("main.html", logstatus=log_stat, posts=posts_, comment_url=comment_url, edit_url=edit_url,
                    delete_url=delete_url)
                

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
        
        result = check(username_, password_, password_, "oren@oren.com", False)
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
            print "oren-11"
            sys.stdout.flush()
            self.render("signin.html", username="", user_error="user don't exist or password don't match[2]",
                        password="", pswd_error="")


class Signout(Handler):
    def get(self):
        self.response.delete_cookie('user')
        self.redirect("/message/7")

# ****************************************************** #
# ****************************************************** #
# ****************************************************** #
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
        print "NewPost post called"
        sys.stdout.flush()
        subject_ = self.request.get('subject')
        content_ = self.request.get('content')
        user = self.request.cookies.get('user',-1)
        postid_= self.request.get('postid')
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
                    print "Inside Post of Newpost - recognized it's a new post"
                    sys.stdout.flush()
                    if content_ and subject_:
                        p = Post(subject=subject_, content=content_, user=dbuser)
                        b_key = p.put()
                        self.redirect("/%d" % b_key.id())
                    else:
                        self.render("addpost.html", subject=subject_, content=content_, error="something is missing",
                                    title="add new post")
                else:# as postid_ is not empty editing existing post.
                    print "Inside Post of Newpost - recognized it's a post edit"
                    sys.stdout.flush()
                    dbpost = Post.get_by_id(int(postid_))
                    print "The value of subject to update is" + subject_
                    sys.stdout.flush()
                    dbpost.subject = subject_
                    dbpost.content = content_
                    dbpost.put()
                    self.redirect("/")
            # cookie is not valid
            else:
                self.redirect("/message/4")

            
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
                print "The user used is GQL: "
                print dbuser
                sys.stdout.flush()
            else:
                log_stat="Not signed in"
                posts_ = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC ")        

        self.render("myposts.html", logstatus=log_stat, posts=posts_)



# This handler deals with the like button and logic
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
                        # updated number of likes in the posts table
                        dbpost.likes = dbpost.likes+1
                        dbpost.put()
                    else: #otherwise - the like is removed or the user is not allowed to like his own
                        for li in existing_likes:
                            li.delete()
                            dbpost.likes = dbpost.likes-1
                            dbpost.put()                   
            else:
                log_stat="Not signed in"

        if check_own=="own":
            self.redirect("/message/6")
        else:
            self.redirect("/")

class AddComment(Handler):
    def post(self):
        user = self.request.cookies.get('user',-1)     
        (cookie_uid,cookie_hash) = user.split("|")
        dbuser = User.get_by_id(int(cookie_uid))
        dbpost = Post.get_by_id(int(self.request.get('postid')))
        comment = self.request.get('comment')
        c = Comment(user=dbuser, post=dbpost, content=comment)
        c.put()
        self.redirect("/"+str(dbpost.key().id()))


# This class is used to present error messages to the user
# To call it you need to call /message/# where # represents the number of the error message
# Then the class renders the message page (message.html) with the appropriate error message
class Message(Handler):
    def get(self,id):
        if id=="1":
            m = "You need to be signed-in to comment on a post.(g)"
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
        self.render("message.html",message=m)

    def post(self,id):
        if id=="1":
            m = "You need to be signed-in to comment on a post.(p)"
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
        self.render("message.html",message=m)

# This handler deals with the edit button and logic
# the main page is rendered in a way that this class will only be called when
# a user is logged in. So we only need to check that the post belongs to the user.
# if the post belongs to the user - we render the add post page with the existing text (to enable modify)
# otherwise we generate an erro saying you can only edit your own posts (2).
class EditPost(Handler):
    def get(self):
        user = self.request.cookies.get('user',-1)     
        (cookie_uid,cookie_hash) = user.split("|")
        dbuser = User.get_by_id(int(cookie_uid))
        postid_=self.request.get('postid')
        dbpost = Post.get_by_id(int(postid_))
        if dbuser.key() == dbpost.user.key():
            self.render("editpost.html", title ="edit post", post=dbpost, postid=postid_)
        else:
            self.redirect("/message/3")

    def post(self):
        subject_ = self.request.get('subject')
        content_ = self.request.get('content')
        postid_= self.request.get('postid')
        user = self.request.cookies.get('user',-1)
        # if there's no cookie
        if user==(-1):
            self.render("signin.html", username="", password="", logstatus="Not signed in", title="add new post")
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):
                dbpost = Post.get_by_id(int(postid_))
                dbpost.subject = subject_
                dbpost.content = content_
                dbpost.put()
                self.redirect("/")
            # cookie is not valid
            else:
                self.redirect("/message/4")

class DeletePost(Handler):
    def get(self):
        user = self.request.cookies.get('user',-1)     
        (cookie_uid,cookie_hash) = user.split("|")
        dbuser = User.get_by_id(int(cookie_uid))
        postid_=self.request.get('postid')
        dbpost = Post.get_by_id(int(postid_))
        if dbuser.key() == dbpost.user.key():
            self.render("deletepost.html", post_title=dbpost.subject, postid=postid_)
        else:
            self.redirect("/message/5")

    def post(self):
        postid_= self.request.get('postid')
        user = self.request.cookies.get('user',-1)
        # if there's no cookie
        if user==(-1):
            self.render("signin.html", username="", password="", logstatus="Not signed in", title="add new post")
        else:
            # check that the cookie is valid
            (cookie_uid,cookie_hash) = user.split("|")
            dbuser = User.get_by_id(int(cookie_uid))
            if dbuser and (dbuser.HashedPassword==cookie_hash):
                dbpost = Post.get_by_id(int(postid_))
                dbpost.delete()
                self.redirect("/")
            # cookie is not valid
            else:
                self.redirect("/message/4")


app = webapp2.WSGIApplication([('/signup', Signup), ('/welcome', Welcome),
                               ('/', Main), ('/login', Signin), ('/logout',Signout),
                               ('/newpost', NewPost), (r'/(\d+)', Permalink),('/like', Like),
                               ('/myposts', MyPosts),('/comment', AddComment),
                               (r'/message/(\d+)', Message), ('/editpost', EditPost),
                               ('/deletepost', DeletePost)], debug=True)
