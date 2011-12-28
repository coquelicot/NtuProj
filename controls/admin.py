from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.webapp.util import run_wsgi_app
from databases.chat import Room

class RoomChecker(webapp.RequestHandler):
    
    def get(self):
        toKill = []
        for room in Room.all():
            if room.ntuuser_set.count() == 0:
                toKill.append(room)
        for room in toKill:
            db.delete(room)

application = WSGIApplication([('/admin/checkRoom', RoomChecker)], debug=True)
