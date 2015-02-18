__author__ = 'Davide Monfrecola'

import numpy

values = [110, 105, 90, 85, 120, 108, 102, 111, 103, 104]

def wma(values, window, weight):
    wma_value = 0
    last = values[0]
    alpha = 0.5
    for value in values:
        wma_value = alpha * value + (1 - alpha) * last
        last = wma_value
    print("####")
    print(wma_value)
    print("####")

def ema(values, window):
    weights = numpy.exp(numpy.linspace(-1., 0., window)) # window = number of samples to generate
    weights /= weights.sum() # the sum of all weights is equal to 1
    a = numpy.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    print(a)
    return a

def ema2():
    ema = []
    ema.append(values[0])
    alpha = 0.5
    for i in range(1, len(values)):
        ema.append(alpha * values[i] + (1 - alpha) * ema[i-1])

    print(ema)