from google.appengine.ext import db

class Counter(db.Model):
	todayVisit = db.IntegerProperty(required=True)
	totalVisit = db.IntegerProperty(required=True)
	lastDate = db.DateProperty(auto_now=True)
