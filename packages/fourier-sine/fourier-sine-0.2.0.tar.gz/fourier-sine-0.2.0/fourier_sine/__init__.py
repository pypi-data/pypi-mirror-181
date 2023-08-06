__version__ = '0.2.0'
import math
from random import choice


def fourier_analysis(series):
    num_elements = len(series)
    coefficients = []
    for period in range(num_elements):
        coefficient_total = 0
        for index in range(num_elements):
            amount = 2*math.pi*index/(1+period)
            coefficient_total += math.sin(amount)*series[index]
        coefficients.append(coefficient_total)
    coefficients = [c/(len(series)/2) for c in coefficients]
    return [0] + coefficients


def create_series(pairs, num_elements, filename=None):
    final_series = [0 for _ in range(num_elements)]
    for pair in pairs:
        for index in range(num_elements):
            final_series[index] = pair[1] * \
                math.sin(2*math.pi*index/pair[0]) + final_series[index]
    if filename is not None:
        series_string = ",".join(str(f) for f in final_series)
        f = open(filename, "w")
        f.write(series_string)
        f.close()
    else:
        return final_series


def create_random_series(filename=None):
    pairs = []
    for _ in range(2):
        pairs.append([choice(range(10, 100)), choice(range(500, 1000))])
        print("frequency", pairs[-1][0], "amplitude", pairs[-1][1])
    length = 1000
    return create_series(filename, pairs, length)


def get_series(filename):
    return [float(f) for f in open(filename, "r").read().split(",")]
