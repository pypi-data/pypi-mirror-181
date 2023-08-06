from scipy import stats
from scipy.optimize import curve_fit
import numpy as np

class Regression:
    @staticmethod
    def linear(x, y, target):
        def _linear(file_data):
            result = stats.linregress(file_data.data[x], file_data.data[y])
            file_data.data[target] = result.slope * file_data.data[x] + result.intercept
            return result
        return _linear

    @staticmethod
    def generic(f, x, y, target):
        def _generic(file_data):
            result = curve_fit(f, file_data.data[x], file_data.data[y])
            file_data.data[target] = f(file_data.data[x], *result[0])
            return result
        return _generic