import urllib
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch_errors

class SendCode(webapp.RequestHandler):

	def post(self):
		try:
			code = self.request.get('code')
			indata = self.request.get('input')
			payload = urllib.urlencode({'code':code.encode('utf-8'), 'input':indata.encode('utf-8')})
			page = urlfetch.fetch('http://toj.tfcis.org/ntucoder/', payload, urlfetch.POST)
			result = page.content
		except urlfetch.InvalidURLError:
			result = 'Can not connect to server.'
		except urlfetch_errors.DeadlineExceededError:
			result = 'Can not get response in time.'
		self.response.out.write(result)
			
application = webapp.WSGIApplication([('/coder/sendCode', SendCode)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
