import uuid
from common.database import Database
import models.users.errors as UserErrors
from common.utils import Utils
import models.users.constants as UserConstants
import models.contacts.constants as ContactConstants

class User(object):
	# def __init__(self, name, email, password, address, ph_no, card_no, orders={}, user_type = "regular", points_earned=0, _id=None):
	# 	self.name = name
	# 	self.email = email
	# 	self.password = password
	# 	self.address = address
	# 	self.ph_no = ph_no
	# 	self.card_no = card_no
	# 	self.user_type = user_type
	# 	self.orders = orders
	# 	self.points_earned = points_earned
	# 	self._id = uuid.uuid4().hex if _id is None else _id
	def __init__(self, name, email, password, address, ph_no, orders={}, user_type = "regular", points_earned=0, _id=None):
		self.name = name
		self.email = email
		self.password = password
		self.address = address
		self.ph_no = ph_no
		self.user_type = user_type
		self.orders = orders
		self.points_earned = points_earned
		self._id = uuid.uuid4().hex if _id is None else _id
		if ContactConstants.checkAdm(self.email)==1:
			print (email)
			while(1):
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
					redirect(url_for('home'))
					break

	def __repr__(self):
		return "<User {}>".format(self.email)

	@staticmethod
	def is_login_valid(email, password):
		user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
		if user_data is None:
			raise UserErrors.UserNotExistsError("Your user does not exist")
		if not Utils.check_hashed_password(password, user_data['password']):
			raise UserErrors.IncorrectPasswordError("Your password is wrong")
		return True

	# @staticmethod
	# def register_user(email, password, name, address, ph_no, card_no):
	# 	user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
	# 	if user_data is not None:
	# 		raise UserErrors.UserAlreadyRegisteredError("The email you used to register already exists.")
	# 	if not Utils.email_is_valid(email):
	# 		raise UserErrors.InvalidEmailError("The email does not have the right format.")
	# 	User(name, email, Utils.hash_password(password), address, ph_no, card_no).save_to_db()
	# 	return True
	@staticmethod
	def register_user(email, password, name, address, ph_no):
		user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
		if user_data is not None:
			raise UserErrors.UserAlreadyRegisteredError("The email you used to register already exists.")
		if not Utils.email_is_valid(email):
			raise UserErrors.InvalidEmailError("The email does not have the right format.")
		User(name, email, Utils.hash_password(password), address, ph_no).save_to_db()
		return True

	def save_to_db(self):
		Database.insert(UserConstants.COLLECTION, self.json())

	def save_to_mongo(self):
		Database.update(UserConstants.COLLECTION, {'_id': self._id}, self.json())

	# def json(self):
	# 	return {
	# 		"_id": self._id,
	# 		"name": self.name,
	# 		"email": self.email,
	# 		"password": self.password,
	# 		"address": self.address,
	# 		"ph_no": self.ph_no,
	# 		"card_no": self.card_no,
	# 		"user_type": self.user_type,
	# 		"orders": self.orders,
	# 		"points_earned": self.points_earned
	# 	}
	def json(self):
			return {
				"_id": self._id,
				"name": self.name,
				"email": self.email,
				"password": self.password,
				"address": self.address,
				"ph_no": self.ph_no,
				"user_type": self.user_type,
				"orders": self.orders,
				"points_earned": self.points_earned
			}

	@classmethod
	def find_by_email(cls, email):
		return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))

	# def get_contents(self):
	# 	return {
	# 		"_id": self._id,
	# 		"name": self.name,
	# 		"email": self.email,
	# 		"password": self.password,
	# 		"address": self.address,
	# 		"ph_no": self.ph_no,
	# 		"card_no": self.card_no,
	# 		"user_type": self.user_type,
	# 		"points_earned": self.points_earned
	# 	}
	def get_contents(self):
		return {
			"_id": self._id,
			"name": self.name,
			"email": self.email,
			"password": self.password,
			"address": self.address,
			"ph_no": self.ph_no,
			"user_type": self.user_type,
			"points_earned": self.points_earned
		}

	def get_user_type(self):
		return self.user_type

	@classmethod
	def get_by_id(cls, id):
		return cls(**Database.find_one(UserConstants.COLLECTION, {"_id": id}))