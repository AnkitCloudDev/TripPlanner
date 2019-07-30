import pymongo

class Database(object):
	URI = "mongodb+srv://ankitdongre96@gmail.com:M0ngo123@mycluster-n3ig0.mongodb.net/test?retryWrites=true&w=majority"
	DATABASE = None

	@staticmethod
	def initialize():
		client = pymongo.MongoClient(Database.URI)
		Database.DATABASE = client['trip_planner']

	@staticmethod
	def insert(collection, data):
		Database.DATABASE[collection].insert(data)

	@staticmethod
	def find(collection, query):
		return Database.DATABASE[collection].find(query)

	@staticmethod
	def find_one(collection, query):
		return Database.DATABASE[collection].find_one(query)

	@staticmethod
	def update(collection, query, data):
		return Database.DATABASE[collection].update(query, data, upsert=True)

	@staticmethod
	def remove(collection, query):
		return Database.DATABASE[collection].remove(query)