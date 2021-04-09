import numpy as np
from functools import cache
import cProfile

class Weights(object):
    def __init__(self, mean, std, sample_size, zeros=0):
        super(Weights, self).__init__()

        self.mean = mean
        self.std = std
        self.sample_size = sample_size
        self.zeros = zeros

        m_total = mean * sample_size
        s_total = std**2. * (sample_size-1) - zeros*(mean**2)
        self.totals_pair = np.array((m_total, s_total))

        self.weights = {}
        self.adjust(1, self.sample_size - self.zeros)
        self.apply_transforms()
    
    def apply_transforms(self):
        while True:
            (score, transform) = self.optimal_transform()
            if score is None or transform[0] == transform[1]:
                return
            else:
                self.adjust(transform[0], -1)
                self.adjust(transform[1])
    
    def optimal_transform(self):
        best_score = None
        best_transform = None
        for value in self.weights.keys():
            base_pair = self.totals_pair + transform(value, self.mean)
            roots = find_optimal(base_pair[0],base_pair[1], self.mean)
            for root in roots:
                new_pair = base_pair - transform(root, self.mean)
                score = self.score(new_pair)
                if best_score == None or score < best_score:
                    best_score = score
                    best_transform = (value, root)
        return (best_score, best_transform)

    def adjust(self, position, shift=1):
        change = transform(position, self.mean)
        self.totals_pair += -1 * shift * change
        self.weights[position] = self.weights.get(position, 0) + shift
        if self.weights[position] == 0:
            del self.weights[position]
    
    def sample(self):
        if self.sample_size <= self.zeros:
            return np.zeros(self.sample_size)

        if self.std == 0:
            return np.repeat(self.mean,self.sample_size)
        
        sample = np.zeros(self.zeros)
        for i,weight in sorted(self.weights.items()):
            sample = np.append(sample, np.repeat(i,int(weight)))

        return sample
    
    def score(self, pair=None):
        if pair is None:
            pair = self.totals_pair
        return (pair**2).sum()

@cache
def transform(x, mean):
    return np.array((x, (x-mean)**2))

@cache
def find_optimal(m_total, s_total, mean):
    a = 108*(m_total - mean)
    b = 6 - 12 * s_total
    c = np.square(a) + 4. * np.power(b,3)
    d = np.lib.scimath.sqrt(c) + a
    e = d.astype(np.cdouble)**(1/3.)

    f = b / (3 * np.cbrt(4) * e)
    g = e / (6 * np.cbrt(2))

    h = 1j*np.sqrt(3)
    x = (1+h)/2
    y = (1-h)/2

    roots = np.array([
        g - f + mean, 
        x*f - y*g + mean, 
        y*f - x*g + mean
    ])
    print(roots)
    reals = np.real(roots[np.isreal(roots)])

    return np.append(np.floor(reals),np.ceil(reals))

# np.set_printoptions(threshold=np.inf)

# pr = cProfile.Profile()
# pr.enable()
# w = Weights(500, 50, 10000)
# print(w.sample())
# pr.disable()
# pr.print_stats(sort='time')

print(Weights(8,8.43115,466).sample())
# print(Weights(8.32184,8.43115,534).sample())

# print(Weights(85453,315001.9136,466).sample())
# print(Weights(113303.84176,315001.9136,534).sample())

# print(Weights(187.324,1239.23439,466).sample())
# print(Weights(195.6264432012,1239.23439,534).sample())