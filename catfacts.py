import webapp2
from google.appengine.ext import db
from google.appengine.api import mail
from TwilioSender import sendWelcome
from CatfactsMember import Member
import twilio

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>')

		q = Member.all()
		if len(list(q.run(limit=51))) > 50:
			self.response.out.write("""
			Sorry, Cat Facts has too many users.
			</body></html>""")
		else:
			self.response.out.write("""
				<form action="/signup" method="post">
					<div>
						Phone Number:<input type="text" name="phone"></textarea> (e.g. 5551234567)
						<input type="submit" value="Sign up for Cat Facts">
					</div>
				</form>
			</body></html>""")

class Members(webapp2.RequestHandler):
	def post(self):
		number = self.request.get('phone')
		if number and len(number) == 10 and number.isdigit():
			ccnumber = "+1" + number
			# find other instances of this
			q = Member.all()
			q.filter("number =", ccnumber)
			member = q.get()

			if member is None:
				m = Member(number = ccnumber)
				m.put()
				sendWelcome(ccnumber)
				self.response.out.write("""
					<html><body>
					Thanks for signing up for Cat Facts!
					</body></html>
				""")
			else:
				self.response.out.write("""
					<html><body>
					You've already signed up for Cat Facts!
					</body></html>
				""")
		else:
			self.response.out.write("""
				<html><body>
				You need to give me a phone number.
				</body></html>
			""")

class Cancel(webapp2.RequestHandler):
	def get(self):
		resp = twilio.twiml.Response()
		resp.sms("Thanks mew!  Your CAT FACTS subscription has been renewed.")
		self.response.out.write(str(resp))

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/signup', Members),
	('/cancel', Cancel)
], debug=True)
