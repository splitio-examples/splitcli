import sys
import time

from splitio import get_factory
from splitio.exceptions import TimeoutException

connection_timeout = 5000
queue_size = 1000000
bulk_size = 20000
all_count = 0

class BatchClient(object):
	def __init__(self, sdk_token):
		super(BatchClient,self).__init__()
		self.factory = None
		try:
			factory = get_factory(sdk_token,config={
				"connectionTimeout": connection_timeout,
				"impressionsQueueSize": queue_size,
				"eventsQueueSize": queue_size, 
				"eventsBulkSize": bulk_size,
				"impressionsBulkSize": bulk_size
			})
			factory.block_until_ready(20)
		except TimeoutException:
			print("SDK failed to initialize")
			sys.exit(1)
		self.split_client = factory.client()

	def get_treatment(self, key, feature):
		global all_count
		treatment = self.split_client.get_treatment(key, feature)
		all_count += 1
		if all_count >= queue_size:
			time.sleep(.5)
			all_count = 0
		return treatment

	def track(self, key, traffic_type, event_type, value, properties):
		success = False
		while not success:
			success = self.split_client.track(key, traffic_type, event_type, value, properties)
			if not success:
				time.sleep(.1)