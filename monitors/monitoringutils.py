__author__ = 'Davide Monfrecola'

'''import numpy

values = [110, 105, 90, 85, 120, 108, 102, 111, 103, 104]

def ema_test(window):
    weights = numpy.exp(numpy.linspace(-1., 0., window)) # window = number of samples to generate
    weights /= weights.sum() # the sum of all weights is equal to 1
    a = numpy.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    print("ema: %s" % a)
'''


def ema_list(values):
    ema_values = [values[0]]
    alpha = 0.5

    for i in range(1, len(values)):
        ema_values.append(alpha * values[i] + (1 - alpha) * ema_values[i-1])

    return ema_values


def ema(value, last_value):
    #print("Current value: {0}".format(value))
    #print("i-1 value: {0}".format(last_value))
    alpha = 0.5
    ema_value = alpha * float(value) + (1 - alpha) * float(last_value)

    print("ema: %s" % ema_value)
    return ema_value