from scipy import stats
from collections import namedtuple
import math

Impact = namedtuple('Impact', ['delta','p_value','mean'])

class EventResult(object):
    def __init__(self, event_type, properties, total_sample):
        super(EventResult, self).__init__()
        self.total_sample = total_sample
        self.event_type = event_type
        self.properties = properties
        self.is_total = None
        self.probability_impact = Impact(0, 1, 1)
        self.count_impact = Impact(0, 1, 1)
        self.value_impact = Impact(0, 1, 0)

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

    def base_events(self, base_sample):
        return self.events(base_sample)

    def comp_events(self, comp_sample):
        p_impact = self.probability_impact.delta
        c_impact = self.count_impact.delta
        v_impact = self.value_impact.delta
        return self.events(comp_sample, p_impact=p_impact, c_impact=c_impact, v_impact=v_impact)

    def events(self, treatment_sample, p_impact=0, c_impact=0, v_impact=0):
        p_mean = min(1, self.probability_impact.mean * (1 + p_impact))
        non_zeros = int(treatment_sample * p_mean)
        
        (count_x, count_y) = self.count_range(treatment_sample, p_impact, c_impact)
        (value_x, value_y) = self.value_range(treatment_sample, p_impact, v_impact)

        events = []
        for i in range(non_zeros):
            count = count_x
            if i%2 == 0:
                count = count_y
            
            value = value_x
            if i%4 < 2:
                value = value_y
            if self.is_total:
                value = value / count
            events.append((count, value))
        
        for _ in range(non_zeros, treatment_sample):
            events.append((0,0))

        return events
    
    def count_range(self, treatment_sample, p_impact=0, c_impact=0):
        p_mean = min(1, self.probability_impact.mean * (1 + p_impact))
        non_zeros = int(treatment_sample * p_mean)
        (target_x, target_y) = self.calculate_range(self.count_impact.delta, self.count_impact.p_value, treatment_sample, p_mean)
        
        # Adjust range to suit mean value
        target_sum = self.count_impact.mean * non_zeros
        actual_sum = math.ceil(non_zeros/2) * target_x + math.floor(non_zeros/2) * target_y
        mean_adjustment = target_sum / actual_sum

        # Adjust range to provide whole numbers
        mean_adj_x = target_x * mean_adjustment
        whole_adjustment = max(1, round(mean_adj_x)) / target_x

        # Shift means to introduce impact
        mean_shift = round(whole_adjustment * c_impact)

        # Adjust and shift range
        count_x = int(whole_adjustment * target_x + mean_shift)
        count_y = int(round(whole_adjustment * target_y) + mean_shift)
        return (count_x, count_y)
    
    def value_range(self, treatment_sample, p_impact=0, v_impact=0):
        p_mean = min(1, self.probability_impact.mean * (1 + p_impact))
        non_zeros = int(treatment_sample * p_mean)

        (target_x, target_y) = (1,1)
        if self.is_total:
            # Accommodate zeros
            (target_x, target_y) = self.calculate_range(self.value_impact.delta, self.value_impact.p_value, treatment_sample, p_mean)
        else:
            # Ignore Zeros
            (target_x, target_y) = self.calculate_range(self.value_impact.delta, self.value_impact.p_value, non_zeros)
        
        # Adjust range to suit mean value
        target_sum = self.value_impact.mean * non_zeros
        actual_sum = math.ceil(non_zeros/2) * target_x + math.floor(non_zeros/2) * target_y
        mean_adjustment = target_sum / actual_sum

        # Shift means to introduce impact
        mean_shift = mean_adjustment * v_impact

        # Adjust and shift range
        value_x = mean_adjustment * target_x + mean_shift
        value_y = mean_adjustment * target_y + mean_shift
        return (value_x, value_y)
    
    # Derivation from: https://www.wolframalpha.com/input/?i=c%3Dn*p%2F2%2C+%28u*s%29%5E2%3D%28c*%28x-u%29%5E2%2Bc*%28y-u%29%5E2%2B%28n*%281-p%29%29*u%5E2%29%2F%28n-1%29%2C+u%3Dc*%28x%2By%29%2Fn%2C+p%3E0%2C+p%3C%3D1%2C+n%3E1%2C+u%3D1%2C+s%3E0+solve+for+x%2Cy
    def calculate_range(self, delta, p_value, treatment_sample, probability=1.0):
        if delta == 0:
            return (1,1)
        if probability == 0 or treatment_sample <= 1:
            raise ValueError("Sample must have multiple non-zero entries")

        # Calculate Variance
        t_out = stats.t.isf(p_value/2.0, self.total_sample-2)
        variance = (self.total_sample * delta**2) / (t_out**2 * 4.0)

        min_variance = treatment_sample * (1 - probability) / (probability * (treatment_sample - 1))
        if variance < min_variance:
            raise ValueError(f"Variance is too small for requested zeros: delta={delta} pvalue={p_value} probability={probability} var={variance} min={min_variance}")

        magic = probability * (variance * (1 - 1 / treatment_sample) + 1) - 1
        x = (1 - math.sqrt(magic))/probability
        y = (1 + math.sqrt(magic))/probability
        return (x, y)