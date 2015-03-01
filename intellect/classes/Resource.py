__author__ = 'Davide Monfrecola'

from monitors.monitoringutils import ema

class Resource(object):

    def __init__(self, resource_id, name="", ema_values={}, command_queue=None):
        self._resource_id = resource_id
        self._name = name
        self._samples = {}
        self._ema_values = ema_values
        self._command_queue = command_queue

        print "created an instance of Resource (id: {0})".format(self.resource_id)

    @property
    def resource_id(self):
        return self._resource_id

    @property
    def name(self):
        return self._name



    @property
    def ema_values(self):
        return self._ema_values

    def add_sample_ema(self, meter, value):
        if meter in self._ema_values.keys():
            ema_value = ema(value, self.ema_values[meter])
            self._ema_values[meter] = ema_value
        else:
            self._ema_values[meter] = value

    def add_sample(self, meter, value):
        if meter in self._samples.keys():
            self._samples[meter] = value
        else:
            self._samples[meter] = value

    def get_sample(self, meter):
        if meter in self._samples.keys():
            return self._samples[meter]
        else:
            return None

    def get_ema(self, meter):
        if meter in self._ema_values.keys():
            return self._ema_values[meter]
        else:
            return None

    def clone(self):
        self._command_queue.put({'command': 'clone', 'resource_id': self._resource_id})
