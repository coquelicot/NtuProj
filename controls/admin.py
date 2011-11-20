from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from dbs.greeting import Greeting

class delGreeting(webapp.RequestHandler):
	def get(self):
		for instance in Greeting.all():
			instance.delete()
		memcache.delete('greetings')
		self.redirect('/')

application = webapp.WSGIApplication([('/admin/del', delGreeting)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
