from google.appengine.ext import db
from user import User

class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    user = db.ReferenceProperty(User, collection_name='blog_posts')
    
    # this is a method that can be called as a property (without ().
    # it uses the post_likes collection which is a reference property in Likes.
    @property
    def plikes(self):
        post_likes = self.post_likes.count()
        return post_likes
        
