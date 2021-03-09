from scipy import stats
import numpy as np
import math

from experiment.measurement.normal_supplier import NormalSupplier
from experiment.measurement.count_supplier import CountSupplier

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
		self.is_sum = None
        self.mean_comparison = self.get_mean_comparison()
        self.deviation = self.get_deviation(self.mean_comparison)

	def probability(self, impact, base=0.5):
		self.probability_base = base
		self.probability_impact = impact
		return self

	def count(self, impact, pval, base=5):
		self.count_mean_base = base
		self.count_impact = impact
		self.count_pval = pval
		return self

	def value(self, impact, pval, base=5):
		if self.is_sum is not None:
			raise ValueError("Value for EventResult is already defined")
		self.value_mean_base = base
		self.value_impact = impact
		self.value_pval = pval
		self.is_sum = False
		return self

	def sum(self, impact, pval, base=5):
		if self.is_sum is not None:
			raise ValueError("Value for EventResult is already defined")
		self.value_mean_base = base
		self.value_impact = impact
		self.value_pval = pval
		self.is_sum = True
		return self

	def generators(self):
		# Probabilities
		comparison_probability = min(self.probability_base * (1 + self.probability_impact/100), 1.0)
		# Counts
		count_result = MeansResult(self.count_mean_base, self.count_impact, self.count_pval, self.sample)
		base_counts = count_result.base_counts(self.probability_base)
		comparison_counts = count_result.comparison_counts(comparison_probability)
		# Values
		value_result = MeansResult(self.value_mean_base, self.value_impact, self.value_pval, self.sample)
		base_values = value_result.base_values()
		comparison_values = value_result.comparison_values()

		base_generator = EventGenerator(self.eventType, self.properties, base_counts, base_values, is_sum=self.is_sum)
		comparison_generator = EventGenerator(self.eventType, self.properties, comparison_counts, comparison_values, is_sum=self.is_sum)
		return (base_generator, comparison_generator)

    def get_mean_comparison(self):
        return self.mean_base * (1.0 + self.impact/100.0)

	
	def mean_lower_bound(self):
		relative_deviation = self.get_relative_deviation()
		return relative_deviation * (sample - 1) / sample * probability / (1 - probability)

    def base_values(self):
        return NormalSupplier(self.mean_base, self.deviation)

    def comparison_values(self):
        return NormalSupplier(self.mean_comparison, self.deviation)

    def base_counts(self, probability):
        return CountSupplier(self.mean_base, self.deviation, probability)

    def comparison_counts(self, probability):
        return CountSupplier(self.mean_comparison, self.deviation, probability)

    def get_relative_deviation(self, impact, pval, sample):
        t_out = stats.t.isf(pval/2.0, sample-2)
        relative_deviation = math.sqrt((sample * impact * impact) / (t_out * t_out * 4.0))
        return relative_deviation
	


	def average(sample, impact, significance, shift=1):
		deviation = get_relative_deviation(impact, significance, sample)
		base_lower = shift - shift * deviation
		base_upper = shift + shift * deviation
		comp_lower = shift * (1+impact) - shift * deviation
		comp_upper = shift * (1+impact) + shift * deviation