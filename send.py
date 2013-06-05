import webapp2
from google.appengine.ext import db
from TwilioSender import sendFact
from CatfactsMember import Member

fact = ""



class MainPage(webapp2.RequestHandler):
	def get(self):
		q = Member.all()
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write(fact)

		for m in q.run(limit=50):
			sendFact(m.number)


application = webapp2.WSGIApplication([
	('/send', MainPage),
], debug=True)
