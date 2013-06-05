import webapp2
from google.appengine.ext import db
from google.appengine.api import mail
from TwilioSender import sendWelcome
from CatfactsMember import Member

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>')

		q = Member.all()
		if len(list(q.run(limit=5))) > 4:
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
				self.redirect('/success')
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

class Success(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
			<html><body>
			Thanks for signing up for Cat Facts!
			</body></html>
		""")

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/signup', Members),
	('/success', Success),
], debug=True)
