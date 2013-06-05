import webapp2
from google.appengine.ext import db
from google.appengine.api import mail



def sendWelcome(email):
	message = mail.EmailMessage(sender="Cat Facts <sjbarag@gmail.com>",
	                            subject="Cat Facts")
	message.to = email
	message.body = "Thank you for subscribing to CAT FACTS!  Every hour, you will receive fun facts about CATS!"

	message.send()

class Member(db.Model):
	email = db.StringProperty(required=True)

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
			gateway = get_gateway(self.request.get('provider'))
			new_email = number+gateway

			# find other instances of this
			q = Member.all()
			q.filter("email =", new_email)
			member = q.get()

			if member is None:
				m = Member(email = new_email, key_name = number)
				m.put()
				sendWelcome(new_email)
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
