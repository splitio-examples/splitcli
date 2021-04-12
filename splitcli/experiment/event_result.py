from scipy import stats
from collections import namedtuple
import numpy as np

from splitcli.experiment.weights import Weights

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

    def events(self, n1, n2):
        p1 = self.probability_impact.mean
        c1 = self.count_impact.mean
        v1 = self.value_impact.mean
        z1 = n1 - int(n1 * p1)

        p2 = min(1, p1 * (1 + self.probability_impact.delta))
        c2 = c1 * (1 + self.count_impact.delta)
        v2 = v1 * (1 + self.value_impact.delta)
        z2 = n2 - int(n2 * p2)

        c_std = self.std_dev(c1,c2,n1,n2,self.count_impact.p_value)
        v_std = self.std_dev(v1,v2,n1,n2,self.value_impact.p_value)

        counts_1 = Weights(c1, c_std, n1, z1).sample()
        counts_2 = Weights(c2, c_std, n2, z2).sample()

        if self.is_total == None:
            values_1 = np.zeros(n1)
            values_2 = np.zeros(n2)
        elif self.is_total == True:
            values_1 = Weights(v1, v_std, n1, z1).sample()
            values_2 = Weights(v2, v_std, n2, z2).sample()
        else:
            values_1 = Weights(v1, v_std, n1 - z1).sample()
            values_1 = np.append(values_1, np.zeros(z1))
            values_2 = Weights(v2, v_std, n2 - z2).sample()
            values_2 = np.append(values_2, np.zeros(z1))
        
        lv1 = len(values_1)
        lc1 = len(counts_1)
        if lv1 != lc1:
            raise ValueError(f"Unmatched result lengths: n1={n1} p1={p1} lv1={lv1} lc1={lc1}")
        
        base_events = self.to_sample(counts_1, values_1)
        comp_events = self.to_sample(counts_2, values_2)

        return (base_events, comp_events)

    def to_sample(self, counts, values):
        sample = []
        for (count,value) in zip(counts, values):
            count = int(count)
            if count == 0:
                value = 0
            elif self.is_total:
                value = value / count
            sample.append((count,value))
        return sample

    def std_dev(self,m1,m2,n1,n2,p_value):
        if m1 == 0:
            return m2-m1
        
        df = n1 + n2 - 2.0
        t_out = stats.t.isf(p_value/2.0, df)
        k = np.sqrt(1./n1 + 1./n2)
        return (m2-m1) / (t_out * k)