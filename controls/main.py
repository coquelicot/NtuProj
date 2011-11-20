import os
import cgi
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from dbs.greeting import Greeting

def getGreetings():
	greetings = memcache.get("greetings")
	if greetings is None:
		greetings = Greeting.gql("order by date desc limit 7")
		if not memcache.add("greetings", greetings):
			logging.error("Memcache set failed.")
	return greetings

class GuestBook(webapp.RequestHandler):

	def post(self):
		user = users.get_current_user()
		if user:
			greeting = Greeting()
			greeting.author = users.get_current_user()
			greeting.content = self.request.get('message')
			greeting.put()
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write(self.request.get('message'))
			memcache.delete("greetings")

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		greetings = getGreetings()
		path = os.path.join(os.path.dirname(__file__), '../templates/chat.html')
		self.response.out.write(template.render(path, {'greetings': greetings}))

class MainPage(webapp.RequestHandler):

	def get(self):

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': users.get_current_user(),
			'url': url,
			'url_linktext': url_linktext,
		}

		path = os.path.join(os.path.dirname(__file__), '../templates/index.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication( [('/', MainPage), ('/show', GuestBook), ('/sign', GuestBook)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
