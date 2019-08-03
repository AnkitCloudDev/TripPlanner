from flask import Blueprint, request, session, url_for, render_template, redirect
from werkzeug.utils import redirect
from models.contacts.contact import Contact
from models.users.user import User
from models.hotels.hotel import Hotel
from models.airlines.airline import Airline
import models.users.errors as UserErrors
import models.users.decorators as user_decorators
import boto3,time
import models.contacts.constants as ContactConstants
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
							
						try:
							response = ContactConstants.sqs.receive_message(
										QueueUrl=ContactConstants.queue_url,
										AttributeNames=[
											'SentTimestamp'
										],
										MaxNumberOfMessages=1,
										MessageAttributeNames=[
											'All'
										],
										VisibilityTimeout=0,
										WaitTimeSeconds=0
										)				
							if 'Messages' in response:
										for msg in response['Messages']:
											# print('Got msg "{0}"'.format(msg['Body']))
												print('got queue message')
							else:
												print('No messages in queue')
												break
										
							print("Try First")
							message = response['Messages'][0]
							print("Try Second")
							Attr=message['MessageAttributes']
							print('before Handle')
							receipt_handle = message['ReceiptHandle']
							print('before Delete')
							# Delete received message from queue will raise error if try to delete from empty queue
							ContactConstants.sqs.delete_message(
													QueueUrl=ContactConstants.queue_url,
													ReceiptHandle=receipt_handle
												)
							#print('Received and deleted message: %s' % message['Body'])
							print (Attr['Sender']['StringValue'])
							# time.sleep(2)
							print (Attr['mail']['StringValue'])
							# time.sleep(1)
							print('MetaData: %s' % message['MessageAttributes'])
							# time.sleep(2)
							print('Received and deleted message: %s' % message['Body'])
							contact = {
									"name": Attr['Sender']['StringValue'],
									"email": Attr['mail']['StringValue'],
									"message": message['Body']
										}
							Contact.save_contact(contact)
						except:
							print("Sorry no messages for you")
							#redirect(url_for('home'))
							break
				return render_template("home.html", user = user)
		except UserErrors.UserError as e:
			return e.message
	return render_template("users/login.html")

@user_blueprint.route('/register', methods=['GET', 'POST'])
# def register_user():
# 	if request.method == 'POST':
# 		name = request.form['name']
# 		email = request.form['email']
# 		password = request.form['password']
# 		address = request.form['address']
# 		ph_no = request.form['ph_no']
# 		card_no = request.form['card_no']
# 		try:
# 			if User.register_user(email, password, name, address, ph_no, card_no):
# 				session['email'] = email
# 				return redirect(url_for(".user_dashboard"))
# 		except UserErrors.UserError as e:
# 			return e.message
# 	return render_template("users/register.html")
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
	contents = user.get_contents()
	return render_template('users/dashboard.html', contents=contents)

@user_blueprint.route('/logout')
def logout_user():
	session['email'] = None
	return redirect(url_for('home'))

# @user_blueprint.route('/contact', methods=['GET', 'POST'])
# def contact_us():
# 	if request.method == 'POST':
# 		name = request.form['name']
# 		email = request.form['email']
# 		message = request.form['message']
		
		# contact = {
		# 	"name": name,
		# 	"email": email,
		# 	"message": message
		# }
		
# 		Contact.save_contact(contact)
# 		return redirect(url_for('home'))
# 	messages = Contact.all_contacts()
# 	return render_template("users/contact.html", messages = messages)

@user_blueprint.route('/contact', methods=['GET', 'POST'])
def contact_us():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		message = request.form['message']
		# while(1):
		response = ContactConstants.sqs.send_message(
				QueueUrl=ContactConstants.queue_url,
				DelaySeconds=10,
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
# @user_blueprint.route('/contact', methods=['GET', 'POST'])
# def sender(name,email,message):
# 		if self.email not in config.ADMINS:
# 			# Send message to SQS queue
# 			response = sqs.send_message(
# 				QueueUrl=ContactConstants.queue_url,
# 				DelaySeconds=10,
# 				MessageAttributes={ #Metadata
# 						'Sender':{
# 						'name':name,
# 						'email':email
# 					}
# 				},
# 				MessageBody=( #Main Message
# 					message
# 				)
# 			)
# 			print(response['MessageId'])
# 	#Code for Receiver Only user can receive