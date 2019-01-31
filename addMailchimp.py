from mailchimp3 import MailChimp



def addToMail(email,site,words):
	'''
	Add the email to our mailchimp list
	'''
	client = MailChimp(mc_api='XXX', mc_user='mattiashem2')
	
	client.lists.members.create('d659e7469a', {
	    'email_address': '{0}'.format(email),
	    'status': 'subscribed',
	    'merge_fields': {
	        'FNAME': '{0}'.format(site),
	        'LNAME': '{0}'.format(words),
	           },
	})
