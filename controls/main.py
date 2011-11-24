import os
import cgi
import logging
import datetime

from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from dbs.greeting import Greeting

class GuestBook(webapp.RequestHandler):

	def post(self):
		user = users.get_current_user()
		if user:
			greeting = Greeting()
			greeting.author = users.get_current_user()
			greeting.content = self.request.get('message')
			# taiwan's timezone: +8
			greeting.date += datetime.timedelta(hours=8)
			greeting.put()
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write(self.request.get('message'))
			memcache.delete("greetingCache")

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		content = memcache.get("greetingCache")
		if content is None:
			greetings = Greeting.gql("order by date desc limit 7")
			path = os.path.join(os.path.dirname(__file__), '../templates/chat.html')
			content = template.render(path, {'greetings': greetings})
			if not memcache.add("greetingCache", content):
				logging.error("Memcache set failed.")
		self.response.out.write(content)

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
