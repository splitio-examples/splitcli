import math

class NormalSupplier(object):
	def __init__(self, mean, deviation):
		super(NormalSupplier, self).__init__()
		self.mean = mean
		self.deviation = deviation
		self.runningCount = 0
		self.runningSum = 0
		self.runningDistanceSquare = 0

	def sample(self):
		smp = self.sampleInterval()
		self.trackSample(smp)
		return smp

	def sampleInterval(self):
		if self.runningCount == 0:
			return self.mean
		elif self.deviation == 0:
			return self.mean
		else:
			ideal_next = self.idealNextForMean()
			dev_distance = self.deviationDistance()

			if ideal_next > self.mean:
				return self.mean + dev_distance
			else:
				return self.mean - dev_distance

	def trackSample(self, sample):
		self.runningCount += 1
		self.runningSum += sample
		self.runningDistanceSquare += (sample - self.mean) * (sample - self.mean)

	def idealNextForMean(self):
		return (self.runningCount + 1) * self.mean - self.runningSum

	def deviationDistance(self):
		if self.runningCount == 0:
			return self.mean

		return math.sqrt(abs((self.deviation ** 2) * self.runningCount - self.runningDistanceSquare))