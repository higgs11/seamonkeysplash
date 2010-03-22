from google.appengine.ext import db

class ControlModule(db.Model):
    author = db.UserProperty()
    wins = db.IntegerProperty()
    losses = db.IntegerProperty()
    name = db.StringProperty()   
    date = db.DateTimeProperty(auto_now_add=True)