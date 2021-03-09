class EventGenerator(object):
	def __init__(self, event_type, properties, count_supplier, value_supplier, is_sum=False):
		super(EventGenerator, self).__init__()
		self.event_type = event_type
		self.properties = properties
		self.count_supplier = count_supplier
		self.value_supplier = value_supplier
		self.is_sum = is_sum

	def events(self, split_client, key, position):
		value = self.value_supplier.sample()
		count = int(self.count_supplier.sample())
		if self.is_sum:
			value = value / count
		for _ in range(0, count):
			split_client.track(key, "user", self.event_type, value, self.properties)

	def __str__(self):
		return str({
			"event_type": self.event_type,
			"properties": self.properties,
			"count": self.count_supplier.__dict__,
			"value": self.value_supplier.__dict__
		})