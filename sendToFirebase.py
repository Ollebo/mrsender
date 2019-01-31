from firebase import firebase
import json
import os
import datetime



import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/code/fins-dff79-firebase-adminsdk-lozi2-715a0adc3f.json')
USER_ID='7qwtyt4vTqN5OWdeTaLWsfcfALH2'
MATCH='wordpress'
MAILCHIMP_LIST="5555"

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fins-dff79.firebaseio.com'
})



ref = db.reference('todos/'+USER_ID+'/emails')
ref_user = db.reference('todos/'+USER_ID+'/emails')
db_values = ref_user.get()
for values in db_values:
	for values2 in db_values[values]:
		#print(values2)
		if values2 == "words":
			if MATCH in db_values[values][values2]:
				'''
				Great we have a email and that matched the words we are using lets add it to the mailchimp list
				'''
				print(db_values[values]['EmailCampan'])


				#Lest se if we already have sent a email to this person
				if MAILCHIMP_LIST in db_values[values]['EmailCampan']:
					print("We habe already used this email here")

				else:
					'''
					Nice lets add the email to the list and update profile
					'''
					user = db_values[values]
					box_ref = ref.child(values)
					list_list=db_values[values]['EmailCampan']
					list_list.append(MAILCHIMP_LIST)
					updated =box_ref.update({
    							'EmailCampan': list_list
							}) 

					print(updated)


				print(db_values[values])


