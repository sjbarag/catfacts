from google.appengine.ext import db

class Member(db.Model):
	number = db.StringProperty(required=True)
