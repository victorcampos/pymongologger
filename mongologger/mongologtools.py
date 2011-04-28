import pymongo
from bson.code import Code
from datetime import datetime

class MongoLogger:
	"""
	Manages MongoDB connection and click logging facilities.
	"""
	
	connection = None
	db = None
	collection = None
	
	def __init__(self, host='localhost', port=27017, db=None, collection=None):
		"""
		Should specify a database name through 'db' and collection names 
		through 'collection', otherwise no connection is made.
		"""
		self.connection = pymongo.Connection(host=host, port=port)
		
		if db != None and collection != None:
			self.db = self.connection[db]
			self.collection = self.db[collection]
			
			self.collection.create_index("ad_id")
			self.collection.create_index([("ad_id", pymongo.ASCENDING), ("date", pymongo.DESCENDING), ("hour", pymongo.DESCENDING)])
		
	def log(self, ad_id=None):
		"""
		Logs a new entry for ad_id to MongoDB in current date/hour.
		"""
		now = datetime.now()
		entry = { "ad_id" : ad_id, "date" : now.date().isoformat(), "hour" : now.hour }
		update_data = { "$inc" : { "clicks" : 1 } }
		
		self.collection.update(entry, update_data, upsert=True)
	
	def fetch(self, ad_id=None, start_date=None, end_date=None, total=False):
		"""
		Fetchs and summarizes log data for given 'ad_id' between 'start_date' 
		and 'end_date' (inclusive).
		If 'total' is set to True it overrides the default behavior from
		summarizing clicks per day to computing a sum of clicks in the
		give range by 'start_date' and 'end_date'.
		"""
		if ad_id != None and start_date != None and end_date != None:
			if total == False:
				map = Code(
					"function() {"
					"	emit(this.date, this.clicks);"
					"}")
			else:
				map = Code(
					"function() {"
					"	emit(1, this.clicks);"
					"}")

			reduce = Code(
						"function(k, vals) {"
						"	var total = 0;"
						"	for (i in vals) {"
						"		total += vals[i];"
						"	}"
						"	return total;"
						"}")
						
			query = { "ad_id" : ad_id, "date" : { "$gte" : start_date.isoformat(), "$lte" : end_date.isoformat() } }
			
			result = self.collection.map_reduce(map, reduce, out="results", query=query)
			
			result_arr = []
			
			if total == False:
				for doc in result.find():
					result_arr.append({ "date" : doc["_id"], "total" : doc["value"] })
			else:
				doc = result.find_one()
				result_arr.append({ "total" : doc["value"] })
				
			return result_arr