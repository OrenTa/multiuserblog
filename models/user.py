from google.appengine.ext import db

class User(db.Model):
    Name = db.StringProperty(required=True)
    HashedPassword = db.StringProperty(required=True)
    Email = db.StringProperty(required=False)
