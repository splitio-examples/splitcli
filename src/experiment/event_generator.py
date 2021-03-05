all_count = 0

class EventGenerator(object):
	def __init__(self, event_type, properties, count_supplier, value_supplier):
		super(EventGenerator, self).__init__()
		self.event_type = event_type
		self.properties = properties
		self.count_supplier = count_supplier
		self.value_supplier = value_supplier

	def events(self, split_client, key, position):
		print("Here")
		global all_count
		value = self.value_supplier.sample()
		count = int(self.count_supplier.sample())
		for i in range(0, count):
			print(all_count)
			all_count += 1
			result == False
			while result == False:
				result = split_client.track(key, "user", self.event_type, value, self.properties)
				if result == False:
					print(split_client._events_storage.__dict__)
					print(split_client._events_storage._events.__dict__)

	def __str__(self):
		return str({
			"event_type": self.event_type,
			"properties": self.properties,
			"count": self.count_supplier.__dict__,
			"value": self.value_supplier.__dict__
		})