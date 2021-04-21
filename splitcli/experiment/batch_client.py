import sys
import time
import threading

from splitio import get_factory
from splitio.exceptions import TimeoutException

from splitcli.ux import menu

connection_timeout = 5000
queue_size = 1000000
bulk_size = 20000
all_count = 0

class BatchClient(object):
	def __init__(self, sdk_token):
		super(BatchClient,self).__init__()
		try:
			self.factory = get_factory(sdk_token,config={
				"connectionTimeout": connection_timeout,
				"impressionsQueueSize": queue_size,
				"eventsQueueSize": queue_size, 
				"eventsBulkSize": bulk_size,
				"impressionsBulkSize": bulk_size,
				"impressionsMode": "optimized"
			})
			self.factory.block_until_ready(20)
		except TimeoutException:
			menu.error_message("SDK failed to initialize")
			sys.exit(1)
		self.split_client = self.factory.client()

	def get_treatment(self, key, feature, attributes={}):
		global all_count
		treatment = self.split_client.get_treatment(key, feature, attributes)
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
				print(key, traffic_type, event_type, value, properties)
				time.sleep(.1)
	
	def destroy(self):
		stop_event = threading.Event()
		self.factory.destroy(stop_event)
		stop_event.wait()