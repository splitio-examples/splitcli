
event_registry = {}

def register_event(metric, delta=0, p_value=1, mean=1):
    property -> property_filter -> probability, count; property -> value

values = []

class EventValueSupplier(object):
    def __init__(self, property, delta, p_value, mean=1):
        super(EventValueSupplier, self).__init__()
        self.property = property
        self.is_total = None
        self.delta = delta
        self.p_value = p_value

    def value_range(self, treatment_sample, p_mean, p_impact=0, v_impact=0):
        p_mean = min(1, p_mean * (1 + p_impact))
        non_zeros = int(treatment_sample * p_mean)

        (target_x, target_y) = (1,1)
        if self.is_total:
            # Accommodate zeros
            (target_x, target_y) = self.calculate_range(self.delta, self.p_value, treatment_sample, p_mean)
        else:
            # Ignore Zeros
            (target_x, target_y) = self.calculate_range(self.delta, self.p_value, non_zeros)
        
        # Adjust range to suit mean value
        target_sum = self.mean * non_zeros
        actual_sum = math.ceil(non_zeros/2) * target_x + math.floor(non_zeros/2) * target_y
        mean_adjustment = target_sum / actual_sum

        # Shift means to introduce impact
        mean_shift = mean_adjustment * v_impact

        # Adjust and shift range
        value_x = mean_adjustment * target_x + mean_shift
        value_y = mean_adjustment * target_y + mean_shift
        return (value_x, value_y)