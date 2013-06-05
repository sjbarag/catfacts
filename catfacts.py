import webapp2
from google.appengine.ext import db
from google.appengine.api import mail



def sendText():
	message = mail.EmailMessage(sender="Cat Facts <sjbarag@gmail.com>",
	                            subject="Cat Facts")
	message.to = "2153808844@txt.att.net"
	message.body = "Thank you for subscribing to CAT FACTS!  Every hour, you will receive fun facts about CATS!"

	message.send()

class Member(db.Model):
	email = db.EmailProperty(required=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>')

		self.response.out.write("""
			<form action="/signup" method="post">
				<div>Phone Number:<input type="text" name="phone"></textarea></div>
				<div>Provider:
					<select name="provider">
						<option value="att">AT&T</option>
						<option value="tmo">T-Mobile</option>
						<option value="vzw">Verizon</option>
						<option value="spr">Sprint</option>
					</select>
				</div>
				<div><input type="submit" value="Sign up for Cat Facts"></div>
			</form>
		</body></html>""")

def get_gateway(provider):
	return {
			"att": "@txt.att.net",
			"tmo": "@tmomail.net",
			"vzw": "@vtext.com",
			"spr": "@messaging.sprintpcs.com"
		}.get(provider, "")

class Members(webapp2.RequestHandler):
	def post(self):
		number = self.request.get('phone')
		if number and len(number) == 10 and number.isdigit():
			phone_k = db.Key.from_path('Employee', number)
			member = db.get(phone_k)
			if not member:
				gateway = get_gateway(self.request.get('provider'))
				if gateway:
					m = Member(email = db.Email(number+gateway), key_name = number)
					m.put()
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
		sendText()
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
