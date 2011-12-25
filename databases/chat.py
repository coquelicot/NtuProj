from google.appengine.ext import db

class Room(db.Model):
	name = db.StringProperty()

class NtuUser(db.Model):
	user = db.UserProperty()
	room = db.ReferenceProperty(Room)
	timestamp = db.IntegerProperty()

class Message(db.Model):
	user = db.ReferenceProperty(NtuUser)
	room = db.ReferenceProperty(Room)
	text = db.TextProperty()
	time = db.DateTimeProperty(auto_now_add=True)

