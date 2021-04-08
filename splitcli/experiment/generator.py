from scipy import stats, optimize
import numpy as np
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
        values_1 = np.append(values_1, [0 for _ in range(z1)])
        values_2 = create_sample(v2, v_std, n2 - z2)
        values_2 = np.append(values_2, [0 for _ in range(z2)])
    
    lv1 = len(values_1)
    lc1 = len(counts_1)
    if lv1 != lc1:
        raise ValueError(f"Unmatched result lengths: n1={n1} p1={p1} lv1={lv1} lc1={lc1}")
    
    sample1 = []
    for (count,value) in zip(counts_1, values_1):
        if count == 0:
            value = 0
        elif event_result.is_total:
            value = value / count
        sample1.append((value,count))
    
    sample2 = []
    for (count,value) in zip(counts_2, values_2):
        if count == 0:
            value = 0
        elif event_result.is_total:
            value = value / count
        sample2.append((value,count))
    return {
        'sample1': sample1,
        'sample2': sample2
    }

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
    print(m,std,n,zeros)
    return []
    # if n <= zeros:
    #     return [0 for _ in range(n)]
    
    # if std == 0:
    #     return [m for _ in range(n)]
    
    # non_zeros = n - zeros
    # subset = best_factor(non_zeros)
    # repeater = non_zeros / subset
    
    # m_total = m * n / repeater
    # s_total = (std**2 * (n-1) - zeros*(m**2)) / repeater
    
    # global leaves
    # leaves = 0
    # result = search_weights(m_total, s_total, m, subset)
    # print(leaves)
    # print(m, std, n)
    # result = to_sample(result)
    # sample = np.repeat(result, repeater)
    # sample = np.append(sample, [0 for _ in range(zeros)]) # Add zeros
    # np.set_printoptions(threshold=np.inf)
    # return sample

def best_factor(n):
    for i in range(10,100):
        if n % i == 0:
            return i
    
    if(subset_nz > 100):
        raise ValueError(f"Factors of N are too big: n={n} nz={non_zeros} subset={subset_nz}")

leaves = 0

def search_weights(m_total, s_total, m, n):
    max_value = min(int(np.ceil(m_total-(n-1))), int(np.ceil(np.sqrt(abs(s_total))+m)))
    return search_weights_recursive(m_total, s_total, m, max_value, n, 0)


best_score = None

def score_func(m_total, s_total, m):
    def score(weights):
        nm_total, ns_total = 0,0
        for i,w in enumerate(weights):
            x = i+1
            nm_total += w * x
            ns_total += w * (m-x)**2
        return abs(m_total)**2 + abs(s_total)
    return score

def transforms(max_value, mean):
    t_map = { }
    for i in range(max_value):
        for j in range(max_value):
            if i != j:
                m_delta = j-i
                s_delta = (j-mean)**2 - (i-mean)**2
                m_increase = m_delta >= 0
                s_increase = s_delta >= 0
                key = (i, m_increase, s_increase)
                t = t_map.get(key,[])
                t.append((j, m_delta, s_delta))
                t_map[key] = t
    return t_map

@cache
def search_weights_recursive(m_total, s_total, m, max_value, remaining, position):
    global best_score
    global leaves

    if remaining == 0:
        leaves += 1
        score = score_state(m_total, s_total)
        if best_score == None or score < best_score:
            best_score = score
            return [0 for _ in range(max_value)]
        else:
            return None
    
    if position >= max_value:
        return None

    best_weights = None
    for k in range(remaining+1):
        x = position + 1
        nm_total = m_total - k * x
        ns_total = s_total - k * (m-x)**2
        if best_score != None and score_inc(nm_total, ns_total) > best_score:
            continue
        weights = search_weights_recursive(nm_total, ns_total, m,max_value, remaining - k, position+1)
        if weights != None:
            best_weights = weights
            best_weights[position] = k
            if best_score == 0:
                return best_weights
    return best_weights

def score_state(m_total, s_total):
    return abs(m_total)+ abs(s_total)

def score_inc(m_total, s_total):
    return max(-m_total,-s_total)

def to_sample(weights):
    sample = []
    for i,weight in enumerate(weights):
        x = i+1
        sample.extend([x for _ in range(int(weight))])
    return sample

@cache
def search_for_sample(m_total, s_total, m, n, curr_x=1):
    global leaves
    if n == 0:
        leaves += 1
        # TODO: Success metric should be (1) preserving the ratio between mean and std (2) preserving ratio between m1 and m2
        return (abs(m_total)**2 + abs(s_total), [])

    mn = curr_x
    mx = int(np.ceil(m_total-(n-1)))
    mx = min(int(np.ceil(m_total-(n-1))), int(np.ceil(np.sqrt(abs(s_total))+m)))
    mstep = 1
    if mx > 100:
        mstep = int(max(1,np.floor((mx - mn) / 10)))

    best_score = None
    best_res = None
    for x in range(mn,mx+1, mstep):
        nm_total = m_total - x
        ns_total = s_total - (x-m)**2

        m_score = min_dist(nm_total, ns_total, m, n-1)
        if best_score is not None and (m_score > best_score or best_score * -1 > m_total or best_score * -1 > s_total):
            continue
        (score, res) = search_for_sample(nm_total, ns_total, m, n-1,x)
        if score is not None and (best_score is None or score < best_score):
            best_score = score
            best_res = np.append(res, x)
            if score == 0:
                return(best_score, best_res)
    
    return (best_score, best_res)

@cache
def min_dist(u_total, s_total, m, n):
    min_u = n
    min_s = n*(round(m) - m)**2
    
    max_s = (n-1)*(1-m)**2 + (u_total - (n-1) - m)**2
    return max(min_u - u_total, min_s - s_total, s_total - max_s, 0)



def linear_search(m_total, s_total, m, n, curr_x=1):
    mx = int(np.ceil(m_total-(n-1)))

    m_var = []
    s_var = []
    c_var = []
    for x in range(mx):
        m_var.append(x)
        s_var.append((x-m)**2)
        c_var.append(1)
    
    Aub = [m_var, s_bar]
    bub = [m_total, s_total]
    Aeq = [c_var]
    beq = [n]


def distance(moments, mu, sigma, n):
    m_dist = mu - moments[0]
    s_dist = sigma - moments[1]

    return m_dist **2 + s_dist **2

def corrector(mu, sigma, n):
    upper = int(mu*n)
    guess = [0 for _ in range(upper)]

    target = np.array([mu, sigma])
    result = optimize.minimize(
        lambda x: distance(updated_moments(x, mu, sigma, n), mu, sigma, n),
        x0=guess,
        constraints=[
            {'type':'eq','fun': lambda x: count_constraint(x,n)}
        ],
        bounds=count_bounds(upper,n),
        options={
            'maxiter':1000,
            'disp': True,
            'eps': 1
        }
    )
    print(result)
    sample = []
    for i,weight in enumerate(result.x):
        x = i+1
        sample.extend([x for _ in range(int(weight))])
    return sample

def updated_moments(weights, mu, sigma, n):
    print(weights)
    n_total, m_total, s_total = 0,0,0
    for i, weight in enumerate(weights):
        x = i+1
        k = int(weight)
        n_total += k
        m_total += k * x
        s_total += k * (mu-x)**2
    
    new_mu = m_total / n
    new_sigma = s_total / (n-1)

    sample = []
    for i,weight in enumerate(weights):
        x = i+1
        sample.extend([x for _ in range(int(weight))])
    print(sample)
    print(distance((new_mu, new_sigma), mu, sigma, n))

    return (new_mu, new_sigma)

def corrector_v(mu, sigma, n):
    upper = int(mu*n)
    guess = [1 for _ in range(n)]

    target = np.array([mu, sigma])
    result = optimize.minimize(
        lambda x: distance(updated_moments_v(x, mu, sigma, n), mu, sigma, n),
        x0=guess,
        bounds=count_bounds_v(upper,n),
        jac=[1 for _ in range(n)],
        options={
            'maxiter':1000,
            'disp': True,
            'eps': 1
        }
    )
    print(result)
    return result.x

def count_constraint(weights, n):
    total = 0
    for weight in weights:
        total += int(weight)
    return total - n

def count_bounds(upper, n):
    return [[0,n] for _ in range(int(upper))]

# print(corrector(2.2, 1, 10))


events(EventResult("test").count(.04023,.5472,8), 5012, 4988)
# print(create_sample(2.2, 1, 10))
