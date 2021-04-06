from scipy import stats
from collections import namedtuple
import math

Impact = namedtuple('Impact', ['delta','p_value','mean'])

class EventResult(object):
    def __init__(self, event_type, properties={}, property_value=None):
        super(EventResult, self).__init__()
        self.event_type = event_type
        self.properties = properties
        self.is_total = None
        self.probability_impact = Impact(0, 1, 1)
        self.count_impact = Impact(0, 1, 1)
        self.value_impact = Impact(0, 1, 0)
        self.property_value = property_value

    def probability(self, delta=0, p_value=1, mean=1):
        self.probability_impact = Impact(delta, p_value, mean)
        return self

    def count(self, delta=0, p_value=1, mean=1):
        self.count_impact = Impact(delta, p_value, mean)
        return self

    def average(self, delta=0, p_value=1, mean=0):
        if self.is_total is not None:
            raise ValueError("Can not set both total and average")
        self.value_impact = Impact(delta, p_value, mean)
        self.is_total = False
        return self

    def total(self, delta=0, p_value=1, mean=0):
        if self.is_total is not None:
            raise ValueError("Can not set both total and average")
        self.value_impact = Impact(delta, p_value, mean)
        self.is_total = True
        return self