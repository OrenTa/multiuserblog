from google.appengine.ext import db
from user import User
from post import Post

class Comment(db.Model):
    user = db.ReferenceProperty(User, collection_name='user_comments')
    post = db.ReferenceProperty(Post, collection_name='post_comments')
    content = db.StringProperty(required=True)
