import numpy as np
from functools import lru_cache

class Weights(object):
    def __init__(self, mean, std, sample_size, zeros=0, is_count=True):
        super(Weights, self).__init__()

        self.mean = mean
        self.std = std
        self.sample_size = sample_size

        # Count metrics require positive integers
        self.is_count = is_count

        # The probability of a metric requires that some of the values be 0
        # All remaining values (for count metrics) must be positive integers
        self.zeros = zeros

        # We can focus on reaching specific totals for mean and standard deviation based on x
        # Removing sample_size from the equation lets us focus on reducing those totals to 0
        m_total = mean * sample_size # sum(x) = mean * sample_size
        s_total = std**2. * (sample_size-1) # sum((x-m)^2) = std**2 * (sample_size-1)        
        s_total -= zeros*(mean**2) # As zeros are pre-set, we can remove them now (mean total is unaffected by zeros)
        self.totals_pair = np.array((m_total, s_total))

        # Weights are pairs between some value x and how many times that value appears in the data
        # { 1:5, 2:3, 5:2 } would mean a sample of [ 1 1 1 1 1 2 2 2 5 5 ]
        # Initialize the sample weights to be all 1s
        self.weights = {}
        self.adjust(1, self.sample_size - self.zeros)
        self.apply_transforms()
    
    def apply_transforms(self):
        while True:
            # Identify the best way to transform the existing sample
            transform = self.optimal_transform()
            if transform is None or transform[0] == transform[1]:
                # When no transform improves the sample, we are done
                return
            else:
                # Otherwise, apply the transformation
                self.adjust(transform[0], -1)
                self.adjust(transform[1])
    
    def optimal_transform(self):
        # A transform involves replacing an existing value in the sample with a new one
        
        # Transform must beat the distribution's current score
        best_score = self.score()
        best_transform = None

        # To replace a value, first we must remove an existing one
        # This iterates over the unique values in the sample
        for removed_value in self.weights.keys():
            # Identify the state of the sample with this value removed
            base_pair = self.totals_pair - transform(removed_value, self.mean)

            # Find the best values to replace the removed value with
            roots = find_optimal(base_pair[0],base_pair[1], self.mean, self.is_count)
            for added_value in roots:
                new_pair = base_pair + transform(added_value, self.mean)
                # If this new value is better than any other (or not changing)
                # Track that as the new best transformation
                score = self.score(new_pair)
                if score < best_score:
                    best_score = score
                    best_transform = (removed_value, added_value)
        return best_transform

    def adjust(self, x, shift=1):
        # x represents the value being added or removed from the data
        # shift represents how many of that value are being added or removed
        #   1 means add one x to the sample, -2 means remove 2 x's from the sample

        # Identify how this new value will impact the mean and standard deviation
        # Increment the state by that change
        self.totals_pair += shift * transform(x, self.mean)

        # Add or remove the value from the sample
        self.weights[x] = self.weights.get(x, 0) + shift

        # Remove value from weights if it has zero elements
        # Makes testing of values to remove more efficient
        if self.weights[x] == 0:
            del self.weights[x]
    
    def sample(self):
        # Convert the weights data into the sample array

        # If it is all zeros, ignore the weights
        if self.sample_size <= self.zeros:
            return np.zeros(self.sample_size)

        # Start the sample with all zeros
        sample = np.zeros(self.zeros)

        # If there is no standard deviation, just return the mean
        if self.std == 0:
            non_zeros = self.sample_size - self.zeros
            sample = np.append(sample, np.repeat(self.mean,non_zeros))
            return sample
        
        for i,weight in sorted(self.weights.items()):
            # Add each value in the sample by its weight
            sample = np.append(sample, np.repeat(i,int(weight)))

        return sample
    
    def score(self, pair=None):
        if pair is None:
            pair = self.totals_pair
        # Calculate the sum of the squared distances
        return (pair**2).sum()
    
    def __str__(self):
        np.set_printoptions(threshold=np.inf)
        sample = self.sample()
        actual_mean = np.average(sample)
        actual_std = np.std(sample, ddof=1)
        actual_n = len(sample)
        output = []
        output.append(f"Means: target={self.mean} actual={actual_mean}")
        output.append(f"Standard Deviation: target={self.std} actual={actual_std}")
        output.append(f"Sample Size: target={self.sample_size} actual={actual_n}")
        if actual_n > 100:
            # Large samples we can output the weights
            output.append(f"Weights: {sorted(self.weights.items())}")
        else:
            output.append(f"Sample: {sample}")
        return "\n".join(output) + "\n"

@lru_cache
def transform(x, mean):
    # Return the impact on the totals caused by adding this value
    # Transformation is reversible, so substracting x will result in subtracting these values
    return -1 * np.array((x, (x-mean)**2))

@lru_cache
def find_optimal(m_total, s_total, mean, is_count):
    # I apologize for this code being a mess, any recommendations to improve it are desired
    # Using np.roots() is way cleaner, but sadly not as efficient

    # This code identifies which values of x will minimize the score from a given state
    # At any time the state has a mean total the sum of the values in the sample
    # At any time the state has a standard deviation total the sum of the squared distances from the mean
    # m_total represents the mean total of the target distribution minus the mean total of the current sample
    # s_total represents the std total of the target distribution minus the std total of the current sample
    # The score heuristic which we seek to minimize is given as: score = m_total**2 + s_total**2
    # When a new value x is added to the sample, the new score is: score = (m_total - x)**2 + (s_total - (x-m)**2)**2
    # To find the values of x which minimize the score, we first take the derivative of the score formula with respect to x
    # Then we solve that formula for x
    # As that derivative is a polynomial with a maximum exponent of x**3, the result has three roots representing inflection points
    # This code calculates those three roots, and returns a positive integer representing their real part
    # The optimal next X to add to the sample will be one of those roots, and the root that yields the highest score will be selected

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

    # Isolates the real portion of the roots, as they may be complex
    # I originally ignored complex numbers but found that their real part can perform better than entirely real roots
    reals = np.real(roots)

    # Count metrics must be positive integers
    if is_count:
        reals = np.round(np.abs(reals)).astype(int)
        reals = reals[reals >= 1]

    return reals