from flask import Blueprint, request, session, url_for, render_template, redirect
import requests
from werkzeug.utils import redirect
from models.contacts.contact import Contact
from models.users.user import User
from models.hotels.hotel import Hotel
from models.airlines.airline import Airline
import models.users.errors as UserErrors
import models.users.decorators as user_decorators
import boto3,time
import models.contacts.constants as ContactConstants
import json
user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods = ['POST', 'GET'])
def login_user():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			if User.is_login_valid(email, password):
				session['email'] = email
				user = User.find_by_email(email)
				print (email)
				#Reciever Code Begins
				if ContactConstants.checkAdm(email)==1:#Check For Admin
					while(1):#Listening for message
							
						try: #Retrieving Message can cause Errors Hence we try to handle it for smooth exec of program
							response = ContactConstants.sqs.receive_message(
										QueueUrl=ContactConstants.queue_url, #queue url for identiying queue
										AttributeNames=[	#Metadata
											'SentTimestamp'
										],
										MaxNumberOfMessages=1,
										MessageAttributeNames=[
											'All'
										],
										VisibilityTimeout=0,
										WaitTimeSeconds=0
										)				
							if 'Messages' in response: #Checking for Messages
										for msg in response['Messages']:
											# print('Got msg "{0}"'.format(msg['Body']))
												print('got queue message')
							else:
												print('No messages in queue')
												break
							
							print("Try First")
							message = response['Messages'][0] # Storing 1st message from response in message
							print("Try Second")
							Attr=message['MessageAttributes'] # Retrieving metadata from message 
							print('before Handle')
							receipt_handle = message['ReceiptHandle'] #Receit Handle is generated on receipt of program and is needed for deleting
							#print('before Delete')
							# Delete received message from queue will raise error if try to delete from empty queue
							
							#print('Received and deleted message: %s' % message['Body'])
							print (Attr['Sender']['StringValue'])	#Printing Sender Name from Metadata
							# time.sleep(2)
							print (Attr['mail']['StringValue'])		#Printing Email from Metadata
							# time.sleep(1)
							print('MetaData: %s' % message['MessageAttributes'])
							# time.sleep(2)
							print('Received and deleted message: %s' % message['Body']) #Printing Message 
							contact = {
									"name": Attr['Sender']['StringValue'], 
									"email": Attr['mail']['StringValue'],
									"message": message['Body']
										}
							print("Before Saving")
							Contact.save_contact(contact) #Saving to DB
							print("After Save to DB")
							ContactConstants.sqs.delete_message(	#Deleting Messages only after it is saved to DB
													QueueUrl=ContactConstants.queue_url,
													ReceiptHandle=receipt_handle
												)
							print("Message Deleted")
						except:
							print("Sorry no messages for you") #No message Found
							#redirect(url_for('home'))
							break #Exit loop
				return render_template("home.html", user = user)
		except UserErrors.UserError as e:
			return e.message
	return render_template("users/login.html")

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		address = request.form['address']
		ph_no = request.form['ph_no']
		try:
			if User.register_user(email, password, name, address, ph_no):
				session['email'] = email
				return redirect(url_for(".user_dashboard"))
		except UserErrors.UserError as e:
			return e.message
	return render_template("users/register.html")	

@user_blueprint.route('/dashboard')
def user_dashboard():
	user = User.find_by_email(session['email'])
	response=requests.get("https://pacific-taiga-19477.herokuapp.com/trips/1")#WE are fetching trips thru REST API
	# print("....")
	# print(response.json())
	json_obj=response.json()
	print(json_obj['result'])
	disp=json_obj['result'][0]['destination']
	print(disp)
	res=requests.get("https://pacific-taiga-19477.herokuapp.com/events/1")#we are fetching events from here 
	print("....")
	print(res.json())
	res_n=res.json()
	res_ns=res_n['events'][0]['event_name']
	print(res_ns)
	contents = user.get_contents()
	return render_template('users/dashboard.html', contents=contents, response=json_obj, res=res.json())

@user_blueprint.route('/logout')
def logout_user():
	session['email'] = None
	return redirect(url_for('home'))

@user_blueprint.route('/contact', methods=['GET', 'POST'])
def contact_us():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		message = request.form['message']
		#  Sending Code Begins
		response = ContactConstants.sqs.send_message( #Sending Message
				QueueUrl=ContactConstants.queue_url, #Queue URL
				DelaySeconds=5,
				MessageAttributes={ #Metadata
						'Sender':{
							'DataType': 'String',
							'StringValue': name
						},
						'mail':{
							    'DataType': 'String',
            					'StringValue': email

						}

				},
				MessageBody=( #Main Message
					message
				)
			)
		print(response['MessageId'])
		return redirect(url_for('home')) # if statement ends
	messages = Contact.all_contacts()
	return render_template("users/contact.html", messages = messages)
