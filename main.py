import os
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class Greeting(db.Model):
	author = db.UserProperty()
	content = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)

class GuestBook(webapp.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		greetings = Greeting.all().order('-date').fetch(10)
		path = os.path.join(os.path.dirname(__file__), 'chat.html')
		self.response.out.write(template.render(path, {'greetings': greetings}))

	def post(self):
		greeting = Greeting()
		greeting.author = users.get_current_user()
		greeting.content = self.request.get('message')
		greeting.put()
		self.redirect('/')

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

		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication( [('/', MainPage), ('/sign', GuestBook), ('/show', GuestBook)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
