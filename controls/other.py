import logging
from databases.other import Counter
from databases.chat import NtuUser, Room
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from google.appengine.api import users

enableGetUser = True

class GetVisit(webapp.RequestHandler):
	def post(self):
		result = memcache.get("getVisit")
		if result is None:
			get = Counter.all()
			result = str(get[0].todayVisit) + " " + str(get[0].totalVisit)
			if memcache.set("getVisit", result) == False:
				logging.error("Can not set memcache 'getVisit'")
		self.response.out.write(result)

class Logout(webapp.RequestHandler):
    def get(self):
        ntuusers = NtuUser.gql("where user = :1" ,users.get_current_user())
        if ntuusers.count() > 0:
            user = ntuusers.get()
            lastroom = user.room
            if enableGetUser:
                cacheName = "roomUsers_" + lastroom.name
                logging.error(cacheName)
                memcache.delete(cacheName)
            if lastroom.ntuuser_set.count() == 1 and lastroom.name != "lobby":
                memcache.delete('roomChat_' + lastroom.name)
                db.delete(Message.gql("where Room = :1" ,lastroom))
                db.delete(lastroom)
            user.room = None
            user.put()
        self.redirect(users.create_logout_url('/main'))

application = webapp.WSGIApplication([('/other/getVisit', GetVisit), ('/other/logout', Logout)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
