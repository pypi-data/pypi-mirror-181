import os
import re
import numpy as np

class RegexPatterns:
    UNSIGNED_INT = '\d+'
    UNSIGNED_OPT_INT = '\d*'
    UNSIGNED_FLOAT = f'{UNSIGNED_INT}\.?\d*'
    UNSIGNED_OPT_FLOAT = f'{UNSIGNED_OPT_INT}\.?\d*'

    INT = f'[-+]?{UNSIGNED_INT}'
    OPT_INT = f'[-+]?{UNSIGNED_OPT_INT}'
    FLOAT = f'[-+]?{UNSIGNED_FLOAT}'
    OPT_FLOAT = f'[-+]?{UNSIGNED_OPT_FLOAT}'

def file_names_from_regex(regex=".*", dir=""):
        """
        Returns a list of file names in the given directory that match the given regex.
        """
        pattern = re.compile(regex)
        files = os.listdir(dir)
        return [f'{file}' for file in files if pattern.match(file)]

def sequence(fs):
    """
    Returns a function that applies the given functions in sequence.
    The functions are applied in the order they are given and directly act on the input.
    """
    def function(x):
        for f in fs:
            f(x)
    return function

def pipeline(fs):
    """
    Returns a function that applies the given functions in sequence.
    The functions are applied in the order they are given and the output of one function is the input of the next.
    """
    def function(x):
        for f in fs:
            x = f(x)
        return x
    return function

def one_sigfig_ceil(num):
    # this function takes a value v and returns a and b such that a * 10^b = v with a having one significant figure
    power = np.floor(np.log10(num))
    mantissa = num / 10**power
    return int(mantissa + 1), power

# round a value and its error so that the error has one significant figure
# return separately the rounded value matissa and error mantissa and the power of 10
def round_value_error(value, error):
    error_mantissa, common_power = one_sigfig_ceil(error)
    value_mantissa = round(value / 10**common_power)
    return value_mantissa, error_mantissa, common_power

# take a value and error and return a string in the form "(a ± b) * 10^c"
# take an optional argument toTeX which if true will return a string in the form "$a \pm b \cdot 10^{c}$"
# by default toTeX is True
def format_value_error(value, error, toTeX=False):
    value_mantissa, error_mantissa, common_power = round_value_error(value, error)
    if toTeX:
        return f'({value_mantissa} \pm {error_mantissa}) \cdot 10^{{{common_power}}}'
    else:
        return f'({value_mantissa} ± {error_mantissa}) * 10^{common_power}'