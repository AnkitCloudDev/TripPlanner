import uuid
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
	@staticmethod
	def save_contact(contact):
		Database.insert(ContactConstants.CONTACT, contact)

	@classmethod
	def all_contacts(cls):
		return [cls(**elem) for elem in Database.find(ContactConstants.CONTACT,{})]

	def receiver():
					response = sqs.receive_message(
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
					try:
								message = response['Messages'][0]
								Attr=message['MessageAttributes']
								receipt_handle = message['ReceiptHandle']
								# Delete received message from queue will raise error if try to delete from empty queue
								sqs.delete_message(
									QueueUrl=queue_url,
									ReceiptHandle=receipt_handle
								)
								print(queue_list['QueueUrls'])
								#print('Received and deleted message: %s' % message['Body'])
								print (Attr['Sender']['name'])
								time.sleep(2)
								print (Attr['Sender']['name'])
								time.sleep(1)
								print('MetaData: %s' % message['MessageAttributes'])
								time.sleep(2)
								print('Received and deleted message: %s' % message['Body'])
					except:
								print("Sorry no messages for you",users)
								time.sleep(5)
