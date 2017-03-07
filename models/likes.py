from google.appengine.ext import db
from user import User
from post import Post

class Likes(db.Model):
    user = db.ReferenceProperty(User, collection_name='user_likes')
    post = db.ReferenceProperty(Post, collection_name='post_likes')
