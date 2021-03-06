from common.database import Database
import models.flights.constants as FlightConstants
import uuid
import models.flights.errors as UserErrors

class Flight(object):

	def __init__(self, location, event_time, total_seats, seats_booked, event_name, price, dates={}, _id = None):
		self.location = location
		self.event_time = event_time
		self.total_seats = int(total_seats)
		self.seats_booked = int(seats_booked)
		self.event_name = event_name
		self.price = price
		self.dates = dates
		self._id = uuid.uuid4().hex if _id is None else _id
	def __repr__(self):
		return "<Plane: {} to {}>".format(self.event_name, self.location)

	def save_to_mongo(self):
		Database.update(FlightConstants.COLLECTION, {"_id": self._id}, self.json())


	def json(self):
			return {
				"location": self.location,
				"event_time": self.event_time,
				"total_seats": self.total_seats,
				"seats_booked": self.seats_booked,
				"event_name": self.event_name,
				"_id": self._id,
				"price": self.price,
				"dates": self.dates
			}

	@classmethod
	def get_by_id(cls, item_id):
		return cls(**Database.find_one(FlightConstants.COLLECTION, {"_id": item_id}))

	@classmethod
	def get_by_airline_id(cls, airline_name):
		return [cls(**elem) for elem in Database.find(FlightConstants.COLLECTION, {"airline_name": airline_name})]

	def get_vacant_seats(self):
		return (self.total_seats - self.seats_booked)

	def get_price(self):
		return self.price

	def delete(self):
		Database.remove(FlightConstants.COLLECTION, {"_id": self._id})

	@classmethod
	def all(cls):
		return [cls(**elem) for elem in Database.find(FlightConstants.COLLECTION,{})]

	@staticmethod
	def is_flight_full():
		raise UserErrors.FlightFull("Sorry! All the seats are full")