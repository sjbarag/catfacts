from twilio import twiml
from twilio.rest import TwilioRestClient
from time import sleep
from math import ceil
from TwilioCreds import *
WELCOME_STRING = "Thank you for subscribing to CAT FACTS!  Every hour, you will receive fun facts about CATS!"

def chunks(s):
	"""Produce 155-character chunks from `s`."""
	page = 0
	totalpages = int(ceil(len(s) / 160.0))
	for start in range(0, len(s), 155):
		page += 1
		if( totalpages > 1 ):
			yield s[start:start+155] +"(%d/%d)" % (page, totalpages)
		else:
			yield s

def sendSMS(number, fact):
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	# messages must be split to 160 characters for use with SMS
	for chunk in chunks(fact):
		client.sms.messages.create(to=number,
		                           from_=TWILIO_NUMBER,
		                           body=fact)
		sleep(2)

def sendWelcome(number):
	sendSMS(number, WELCOME_STRING)
