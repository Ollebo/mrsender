from mailchimp3 import MailChimp
import random
import string

def testMailChimp(MAILCHIMP_API,MAILCHIMP_LIST):
	'''
	Test if we have a working mailchimp connection
	'''
	
	
	client = MailChimp(mc_api=MAILCHIMP_API)

	randomEmail = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
	print(randomEmail)
	mailChimpGood = addToMailchimp('test-api-{0}@mantiser.com'.format(randomEmail),MAILCHIMP_API,MAILCHIMP_LIST)

	if mailChimpGood != False:
		deleteFromMailchimp(mailChimpGood,MAILCHIMP_API,MAILCHIMP_LIST)
		print("mailchimp good")
		return True
	else:
		return False



def deleteFromMailchimp(userhash,MAILCHIMP_API,MAILCHIMP_LIST):
	'''
	Delet the user from the list
	'''
	client = MailChimp(mc_api=MAILCHIMP_API)

	try:
		client.lists.members.delete(list_id=MAILCHIMP_LIST, subscriber_hash=userhash)
	except:
		print('got error from mailchimp')




def addToMail(email,MAILCHIMP_API,MAILCHIMP_LIST):
	'''
	Add the email to our mailchimp list
	'''
	client = MailChimp(mc_api=MAILCHIMP_API)
	
	try:
		client.lists.members.create(MAILCHIMP_LIST, {
		    'email_address': '{0}'.format(email),
		    'status': 'subscribed',
		    'merge_fields': {
		        'FNAME': '{0}'.format(site),
		        'LNAME': '{0}'.format(words),
		           },
		})
		return backFromMailchimp['id']
	except:
		print(backFromMailchimp)
		print("Error update user")
		return False
