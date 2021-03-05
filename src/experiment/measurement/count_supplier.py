import math
from experiment.measurement.normal_supplier import NormalSupplier

class CountSupplier(NormalSupplier):
	def __init__(self, mean, deviation, probability):
		super(CountSupplier, self).__init__(mean, deviation)

		if deviation == 0 and mean != int(mean):
			raise ValueError("Unable to generate fractional mean with no deviation")

		self.probability = probability
		self.zeros = 0

	def sampleInterval(self):
		if self.probability == 0 or self.currentProbability() > self.probability:
			self.zeros += 1
			return 0

		sample = super().sampleInterval()

		if sample != int(sample):
			ideal_next = self.idealNextForMean()
			if sample > ideal_next:
				sample = math.floor(sample)
			else:
				sample = math.ceil(sample)

		if sample <= 0:
			sample = 1

		return sample

	def currentProbability(self):
		if self.runningCount == 0:
			return 0
		return 1 - self.zeros / self.runningCount