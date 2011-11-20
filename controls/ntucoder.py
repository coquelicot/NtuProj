import os
import urllib
import logging
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):

	def show(self, result='', code='', indata=''):
		path = os.path.join(os.path.dirname(__file__), '../templates/coder.html')
		self.response.out.write(template.render(path, {'result':result, 'code':code, 'input':indata}))

	def post(self):
		try:
			code = self.request.get('code')
			indata = self.request.get('input')
			payload = urllib.urlencode({'code':code, 'input':indata})
			page = urlfetch.fetch('http://sincero.dyndns.org/ntuproj/', payload, urlfetch.POST)
			self.show(page.content, code, indata)
		except urlfetch.InvalidURLError:
			self.response.out.write("Can not connect to server.")
			
	def get(self):
		self.show(code='/* code here */')


application = webapp.WSGIApplication([('/ntucoder', MainPage)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
