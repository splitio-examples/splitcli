import random

class PseudoClient(object):
	def __init__(self):
		super(PseudoClient,self).__init__()

	def get_treatment(self, key, feature):
		if bool(random.getrandbits(1)):
			return "on"
		else:
			return "off"

	def track(self, key, traffic_type, event_type, value, properties):
		print({
			"key": key,
			"event_type": event_type,
			"props": properties,
			"value": value
			})