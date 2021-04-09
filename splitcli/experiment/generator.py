from scipy import stats, optimize
import numpy as np
from functools import cache

from splitcli.experiment.event_result import EventResult
from splitcli.experiment.weights import Weights

def events(event_result, n1, n2):
    p1 = event_result.probability_impact.mean
    c1 = event_result.count_impact.mean
    v1 = event_result.value_impact.mean
    z1 = n1 - int(n1 * p1)

    p2 = min(1, p1 * (1 + event_result.probability_impact.delta))
    c2 = c1 * (1 + event_result.count_impact.delta)
    v2 = v1 * (1 + event_result.value_impact.delta)
    z2 = n2 - int(n2 * p2)

    c_std = std_dev(c1,c2,n1,n2,event_result.count_impact.p_value)
    v_std = std_dev(v1,v2,n1,n2,event_result.value_impact.p_value)

    counts_1 = create_sample(c1, c_std, n1, z1)
    counts_2 = create_sample(c2, c_std, n2, z2)

    if event_result.is_total == None:
        values_1 = [0 for _ in range(n1)]
        values_2 = [0 for _ in range(n2)]
    if event_result.is_total == True:
        values_1 = create_sample(v1, v_std, n1, z1)
        values_2 = create_sample(v2, v_std, n2, z2)
    else:
        values_1 = create_sample(v1, v_std, n1 - z1)
        values_1 = np.append(values_1, [0 for _ in range(z1)])
        values_2 = create_sample(v2, v_std, n2 - z2)
        values_2 = np.append(values_2, [0 for _ in range(z2)])
    
    lv1 = len(values_1)
    lc1 = len(counts_1)
    if lv1 != lc1:
        raise ValueError(f"Unmatched result lengths: n1={n1} p1={p1} lv1={lv1} lc1={lc1}")
    
    base_events = to_sample(event_result, counts_1, values_1)
    comp_events = to_sample(event_result, counts_2, values_2)

    return (base_events, comp_events)

def to_sample(event_result, counts, values):
    sample = []
    for (count,value) in zip(counts, values):
        count = int(count)
        if count == 0:
            value = 0
        elif event_result.is_total:
            value = value / count
        sample.append((count,value))
    return sample

def std_dev(m1,m2,n1,n2,p_value):
    if m1 == 0:
        return m2-m1
    effect_size = normalized_effect(p_value, n1, n2)
    return round((m2-m1) / effect_size, 5)

def normalized_effect(p_value, n1, n2):
    df = n1 + n2 - 2.0
    k = np.sqrt(1./n1 + 1./n2)
    t_out = stats.t.isf(p_value/2.0, df)
    # nct_param = nct(.2, t_out, df) 
    # return k * nct_param
    return k * t_out

def nct(beta, t_out, total_sample):
    min_est = 0
    max_est = 12
    for i in range(100):
        guess = (min_est + max_est) / 2.
        result = stats.nct.cdf(t_out, total_sample-2, guess)
        if abs(result - beta) < .00005:
            return guess
        elif result > beta:
            min_est = guess
        else:
            max_est = guess
    return None

def create_sample(m, std, n, zeros=0):
    weights = Weights(m, std, n, zeros)
    weights.apply_transforms()
    return weights.sample()
