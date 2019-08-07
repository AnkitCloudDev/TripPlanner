import uuid
from flask import redirect,url_for
from common.database import Database
import models.contacts.constants as ContactConstants
import config
import boto3

class Contact(object):
	def __init__(self, name, email, message, _id=None):
		self.name = name
		self.email = email
		self.message = message
		self._id = uuid.uuid4().hex if _id is None else _id
		#Receiver Code Begins	
		if ContactConstants.checkAdm(self.email)==1:
			print (email)
			while(1):
				try:
					print("User Reciever Start")			
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
										
								
					print("Try First")
					message = response['Messages'][0]
					print("Try Second")
					Attr=message['MessageAttributes']
					print('before Handle')
					receipt_handle = message['ReceiptHandle']
					print('before Delete')
					# Delete received message from queue will raise error if try to delete from empty queue
					
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
					save_contact(contact)
					print("Saved in Database")
					ContactConstants.sqs.delete_message(
											QueueUrl=ContactConstants.queue_url,
											ReceiptHandle=receipt_handle
										)
					print("Message Deleted Successfully")
				except:
					print("Sorry no messages for you")
					redirect(url_for('home'))
					break

	@staticmethod
	def save_contact(contact):
		Database.insert(ContactConstants.CONTACT, contact)

	@classmethod
	def all_contacts(cls):
		return [cls(**elem) for elem in Database.find(ContactConstants.CONTACT,{})]

