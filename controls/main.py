import os
import datetime
from databases.other import Counter
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

class MainPage(webapp.RequestHandler):
	def get(self):
		memcache.delete('getVisit')
		get = Counter.all()
		if get.count() == 0:
			use = Counter(todayVisit=0, totalVisit=0)
		else:
			use = get.get()
		if use.lastDate != datetime.date.today():
			use.todayVisit = 0
		use.todayVisit += 1
		use.totalVisit += 1
		use.put()
		tmpValue = {'todayVisit':use.todayVisit, 'totalVisit':use.totalVisit, 'myIP':self.request.remote_addr}
		path = os.path.join(os.path.dirname(__file__), '../templates/main.html')
		self.response.out.write(template.render(path, tmpValue))

application = webapp.WSGIApplication([('/main', MainPage)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
