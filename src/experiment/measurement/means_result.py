from scipy import stats
import numpy as np
import math

from experiment.measurement.normal_supplier import NormalSupplier
from experiment.measurement.count_supplier import CountSupplier

class MeansResult(object):
    def __init__(self, mean_base, impact, pval, sample):
        super(MeansResult, self).__init__()
        self.mean_base = mean_base
        self.impact = impact
        self.pval = pval
        self.sample = sample
        self.mean_comparison = self.get_mean_comparison()
        self.deviation = self.get_deviation(self.mean_comparison)

    def get_mean_comparison(self):
        return self.mean_base * (1.0 + self.impact/100.0)

    def get_deviation(self, mean_comparison):
        t_out = stats.t.isf(self.pval/2.0, self.sample-2)
        absolute_impact = mean_comparison - self.mean_base
        deviation = math.sqrt((self.sample * absolute_impact * absolute_impact) / (t_out * t_out * 4.0))
        return deviation

    def base_values(self):
        return NormalSupplier(self.mean_base, self.deviation)

    def comparison_values(self):
        return NormalSupplier(self.mean_comparison, self.deviation)

    def base_counts(self, probability):
        return CountSupplier(self.mean_base, self.deviation, probability)

    def comparison_counts(self, probability):
        return CountSupplier(self.mean_comparison, self.deviation, probability)