from google.appengine.ext import db
from user import User

class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    user = db.ReferenceProperty(User, collection_name='blog_posts')
    likes = db.IntegerProperty(default=0)
