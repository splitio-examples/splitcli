from scipy import stats, optimize
import numpy as np
from functools import cache

class Weights(object):
    def __init__(self, m_total, s_total, mean, n):
        super(Weights, self).__init__()
        self.m_total = m_total
        self.s_total = s_total
        self.totals_pair = np.array((m_total, s_total))
        self.values = set([])

        self.mean = mean
        self.n = n

        self.mx = self.max_value()
        self.weights = np.zeros(self.mx)

        self.adjust(0, n)
    
    def max_value(self):
        m_max = int(np.ceil(self.m_total-(self.n-1)))
        s_max = int(np.ceil(np.sqrt(abs(self.s_total))+self.mean))
        return min(m_max, s_max)
    
    def apply_transforms(self):
        while True:
            (score, transform) = self.optimal_transform()
            if transform[0] == transform[1]:
                return
            else:
                self.adjust(transform[0], -1)
                self.adjust(transform[1])
    
    def optimal_transform(self):
        best_score = None
        best_transform = None
        for value in self.values:
            base_pair = self.totals_pair + transform(value, self.mean)
            for p in range(len(self.weights)):
                new_pair = base_pair - transform(p, self.mean)
                score = self.score(new_pair)
                if best_score == None or score < best_score:
                    best_score = score
                    best_transform = (value, p)
        return (best_score, best_transform)

    def adjust(self, position, shift=1):
        change = transform(position, self.mean)
        self.totals_pair += -1 * shift * change
        self.weights[position] += shift
        if self.weights[position] == 0:
            self.values.remove(position)
        else:
            self.values.add(position)
    
    def sample(self):
        sample = []
        for i,weight in enumerate(self.weights):
            sample.extend(np.repeat(i+1,int(weight)))
        return sample
    
    def score(self, pair=None):
        if pair is None:
            pair = self.totals_pair
        return (pair[0]**2 + abs(pair[1]))

@cache
def transform(i, mean):
    x = i+1
    return np.array((x, (x-mean)**2))

def inst(mean, std, n):
    m_total = mean * n
    s_total = std**2 * (n-1)
    return Weights(m_total, s_total, mean, n)

def create_sample(m, std, n, zeros=0):
    if n <= zeros:
        return np.zeros(n)

    if std == 0:
        return np.repeat(m,n)
    
    non_zeros = n - zeros
    subset = best_factor(non_zeros)
    repeater = non_zeros / subset
    
    m_total = m * n / repeater
    s_total = (std**2 * (n-1) - zeros*(m**2)) / repeater

    weights = Weights(m_total, s_total, m, subset)
    weights.apply_transforms()

    result = weights.sample()
    sample = np.repeat(result, repeater)
    sample = np.append(sample, np.zeros(zeros)) # Add zeros
    return sample

def best_factor(n):
    for i in range(10,100):
        if n % i == 0:
            return i
    
    if(subset_nz > 100):
        raise ValueError(f"Factors of N are too big: n={n} nz={non_zeros} subset={subset_nz}")

np.set_printoptions(threshold=np.inf)
print(create_sample(8,26.73163,5012,0))
print(create_sample(8.32184,26.73163,4988,0))