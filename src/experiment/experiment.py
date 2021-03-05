import time

from experiment.event_result import EventResult

class Experiment(object):
	def __init__(self, sample, feature, comp_treatment="on", key_pattern="user_{position}"):
		super(Experiment, self).__init__()
		self.feature = feature
		self.comp_treatment = comp_treatment
		self.sample = sample
		self.key_pattern = key_pattern
		self.base_generators = []
		self.comp_generators = []

	def event_result(self, eventType, properties):
		return EventResult(eventType, properties, self.sample)

	def register(self, event_result):
		if self.sample != event_result.sample:
			raise ValueError("Invalid sample size")
		(base_generator, comp_generator) = event_result.generators()
		self.base_generators.append(base_generator)
		self.comp_generators.append(comp_generator)
		return self

	def key(self, position):
		return self.key_pattern.format(position=position)

	def base_events(self, split_client, key, position):
		for generator in self.base_generators:
			generator.events(split_client, key, position)

	def comp_events(self, split_client, key, position):
		for generator in self.comp_generators:
			generator.events(split_client, key, position)

	def run(self, split_client):
		print("Creating Experiment")
		for position in range(self.sample):
			key = self.key(position)
			treatment = split_client.get_treatment(key, self.feature)
		time.sleep(.1)
		for position in range(self.sample):
			if position % 1000 == 0:
				print(position)
			key = self.key(position)
			treatment = split_client.get_treatment(key, self.feature)
			if treatment == self.comp_treatment:
				self.comp_events(split_client, key, position)
			else:
				self.base_events(split_client, key, position)