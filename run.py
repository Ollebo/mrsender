import json
import os
import datetime
import time
import random
import string
from mailchimp3 import MailChimp



import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import os

# Fetch the service account key JSON file contents
cred = credentials.Certificate(os.environ['FIREBASE_AUTH'])
USER_ID=os.environ['USER_ID']
MATCH=os.environ['MATCH']
MAILCHIMP_LIST=os.environ['MAILCHIMP_LIST']
MAILCHIMP_API=os.environ['MAILCHIMP_API']
HOW_MANY=int(os.environ['HOW_MANY'])
DELETE_AFTER = os.environ['DELETE_AFTER']
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ['FIREBASE']
})

client = MailChimp(mc_api=MAILCHIMP_API)


userToDelete=[]

def logToUser(message):
	now = datetime.datetime.now()
	print(message)
	log_ref= 	ref = db.reference('/todos/'+USER_ID+'/stats/events')
	data = {
			'message':message,
        	'timestamp': now.isoformat(),
	}
	result = log_ref.push(data)
	print(result)



def startUp():
	'''
	Will start and test if we have conenction to everything. And if not will shut down
	'''
	weGoodToGo=False
	
	## Test Mailchimp
					
	randomEmail = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
	print(randomEmail)
	mailChimpGood = addToMailchimp('test-api-{0}@mantiser.com'.format(randomEmail))

	if mailChimpGood != False:
		print(mailChimpGood)
		deleteFromMailchimp(mailChimpGood)
		print("mailchimp good")
		weGoodToGo = True
	else:
		logToUser('ERROR_SEARCHBOT_MAILCHIMP_ACCESS API_KEY {0} LIST_ID {1}'.format(MAILCHIMP_API,MAILCHIMP_LIST) )
	

	#Lets roll
	if weGoodToGo:
		findAndAddEmail()




def deleteFromMailchimp(userhash):
	'''
	Delet the user from the list
	'''
	try:
		client.lists.members.delete(list_id=MAILCHIMP_LIST, subscriber_hash=userhash)
	except:
		print('got error from mailchimp')


def addToMailchimp(email):
	'''
	Add the email to our mailchimp list
	'''
	backFromMailchimp=""
	try:
		backFromMailchimp=client.lists.members.create(MAILCHIMP_LIST, {
		    'email_address': '{0}'.format(email),
		    'status': 'subscribed',
		    'merge_fields': {
		        'FNAME': '{0}'.format("Automated "),
		        'LNAME': '{0}'.format("Found"),
		           },
		})
		userToDelete.append(backFromMailchimp['id'])
		print(backFromMailchimp)
		return backFromMailchimp['id']

	except:
		print(backFromMailchimp)
		print("Error update user")
		return False


def findAndAddEmail():
	'''
	Here is where we find and add emails
	'''
	logToUser('SEARCHBOT_STARTED MATCH WORDS {0}'.format(MATCH))
	ref = db.reference('todos/'+USER_ID+'/emails')
	ref_user = db.reference('todos/'+USER_ID+'/emails')
	db_values = ref_user.get()
	haveDone=0
	for values in db_values:
		for values2 in db_values[values]:
			if values2 == "words":
				if MATCH in db_values[values][values2]:
					'''
					Great we have a email and that matched the words we are using lets add it to the mailchimp list
					'''
				
	
					#Lest se if we already have sent a email to this person
					haveEmail=False
					try:
						if MAILCHIMP_LIST in db_values[values]['EmailCampan']:
							print("We habe already used this email here")
							haveEmail=True
					except KeyError:
							pass


					if(haveEmail == False):
						'''
						Nice lets add the email to the list and update profile
						'''
						if HOW_MANY >= haveDone:
							user = db_values[values]
							box_ref = ref.child(values)
							try:
								list_list=db_values[values]['EmailCampan']
							except KeyError:
								list_list=[]
							list_list.append(MAILCHIMP_LIST)
							#Add the user to Mailchimp
							addToMailchimp(db_values[values]['email'])
	
							updated =box_ref.update({
	    								'EmailCampan': list_list
									})
	
							#Update how many we have done 
							haveDone=haveDone + 1
							print(updated)
						else:
							print("We have already as many as we need")
	
					print(db_values[values])
				else:
					print("No match in words for email")
					print(str(db_values[values][values2]).encode('utf8'))
					print(MATCH)




	#########################################
	##
	##  Time to clean up and delet the users from the mailchimp list
	
	time.sleep(3)
	if DELETE_AFTER == 'true':
		for user_hash in userToDelete:
			deleteFromMailchimp(user_hash)
	
	logToUser('SEARCHBOT_FINNISH MATCH WORDS {0}'.format(MATCH))

########################################
##
## Function to reset all users list

def clear_emaild_users():
	'''
	Loop and clear out what user has bean to what list


	'''
	ref = db.reference('todos/'+USER_ID+'/emails')
	ref_user = db.reference('todos/'+USER_ID+'/emails')
	db_values = ref_user.get()
	
	for values in db_values:
		for values2 in db_values[values]:
				user = db_values[values]
				print(user)
				box_ref = ref.child(values)
				#Add the user to Mailchimp
				
				updated =box_ref.update({
    						'EmailCampan': ['xxx']
						})

						#Update how many we have done 
				print(updated)
#findAndAddEmail()				
#clear_emaild_users()
#addToMailchimp('matte@ollebo.com')
startUp()