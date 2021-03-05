from experiment.measurement.means_result import MeansResult

from experiment.event_generator import EventGenerator

class EventResult(object):
	def __init__(self, eventType, properties, sample):
		super(EventResult, self).__init__()
		self.sample = sample
		self.eventType = eventType
		self.properties = properties
		# TODO: Change below to a random non-significant default
		self.probability_base = 1
		self.probability_impact = 0
		self.value_mean_base = 0
		self.value_impact = 0
		self.value_pval = .95
		self.count_mean_base = 0
		self.count_impact = 0
		self.count_pval = .95

	def probability(self, base, impact):
		self.probability_base = base
		self.probability_impact = impact
		return self

	def count(self, base, impact, pval):
		self.count_mean_base = base
		self.count_impact = impact
		self.count_pval = pval
		return self

	def value(self, base, impact, pval):
		self.value_mean_base = base
		self.value_impact = impact
		self.value_pval = pval
		return self

	def generators(self):
		# Probabilities
		comparison_probability = max(self.probability_base * (1 + self.probability_impact/100), 1.0)
		# Counts
		count_result = MeansResult(self.count_mean_base, self.count_impact, self.count_pval, self.sample)
		base_counts = count_result.base_counts(self.probability_base)
		comparison_counts = count_result.comparison_counts(comparison_probability)
		# Values
		value_result = MeansResult(self.value_mean_base, self.value_impact, self.value_pval, self.sample)
		base_values = value_result.base_values()
		comparison_values = value_result.comparison_values()

		base_generator = EventGenerator(self.eventType, self.properties, base_counts, base_values)
		comparison_generator = EventGenerator(self.eventType, self.properties, comparison_counts, comparison_values)
		return (base_generator, comparison_generator)
