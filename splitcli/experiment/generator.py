from scipy import stats
import numpy
from functools import cache

from event_result import EventResult

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
        values_1 = numpy.append(values_1, [0 for _ in range(z1)])
        values_2 = create_sample(v2, v_std, n2 - z2)
        values_2 = numpy.append(values_2, [0 for _ in range(z2)])
    
    lv1 = len(values_1)
    lc1 = len(counts_1)
    if lv1 != lc1:
        raise ValueError(f"Unmatched result lengths: n1={n1} p1={p1} lv1={lv1} lc1={lc1}")
    
    data = []
    for (count,value) in zip(counts_1, values_1):
        if count == 0:
            value = 0
        elif event_result.is_total:
            value = value / count
        data.append((value,count))
    return data

def std_dev(m1,m2,n1,n2,p_value):
    if m1 == 0:
        return m2-m1
    effect_size = normalized_effect(p_value, n1, n2)
    relative_difference = (m2-m1) / m1
    print(effect_size, relative_difference)
    return round(effect_size / relative_difference * m1, 5)

def create_sample(m, std, n, zeros=0):
    if n <= zeros:
        return [0 for _ in range(n)]
    
    if std == 0:
        return [m for _ in range(n)]
    
    non_zeros = n - zeros
    subset = best_factor(non_zeros)
    repeater = non_zeros / subset
    
    m_total = m * n / repeater
    s_total = (std**2 * (n-1) - zeros*(m**2)) / repeater
    
    print(m, std, n, zeros)
    print(m_total, s_total, m, subset)
    (score, result) = search_for_sample(m_total, s_total, m, subset)
    print(result)
    sample = numpy.repeat(result, repeater)
    return numpy.append(sample, [0 for _ in range(zeros)]) # Add zeros

@cache
def search_for_sample(m_total, s_total, m, n,curr_x=1):
    global leaves
    if n == 0:
        # TODO: Success metric should be (1) preserving the ratio between mean and std (2) preserving ratio between m1 and m2
        return (abs(m_total)*100 + abs(s_total), [])

    mn = curr_x
    mx = int(numpy.ceil(m_total-n+1))

    best_score = None
    best_res = None
    for x in range(mn,mx+1):
        nm_total = m_total - x
        ns_total = s_total - (x-m)**2

        m_score = min_dist(nm_total, ns_total, m, n-1)
        if best_score is not None and (m_score > best_score or best_score * -1 > m_total or best_score * -1 > s_total):
            continue
        (score, res) = search_for_sample(nm_total, ns_total, m, n-1,x)
        if score is not None and (best_score is None or score < best_score):
            best_score = score
            best_res = numpy.append(res, x)
            if score == 0:
                return(best_score, best_res)
    
    return (best_score, best_res)

def normalized_effect(p_value, n1, n2):
    df = n1 + n2 - 2.0
    k = numpy.sqrt(1./n1 + 1./n2)
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

@cache
def min_dist(u_total, s_total, m, n):
    min_u = n
    min_s = n*(round(m) - m)**2
    
    max_s = (n-1)*(1-m)**2 + (u_total - (n-1) - m)**2
    return max(min_u - u_total, min_s - s_total, s_total - max_s, 0)

def best_factor(n):
    for i in range(10,100):
        if n % i == 0:
            return i
    
    if(subset_nz > 100):
        raise ValueError(f"Factors of N are too big: n={n} nz={non_zeros} subset={subset_nz}")

# print(events(EventResult("test").count(.04023,.5472,8), 100, 100))

std = std_dev(8, 8.3, 100, 100, 0.5472)
print(std)
print(stats.ttest_ind_from_stats(8, std, 100, 8.3, std, 100).pvalue)