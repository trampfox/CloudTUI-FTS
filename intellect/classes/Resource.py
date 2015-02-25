__author__ = 'Davide Monfrecola'

from monitors.monitoringutils import ema

class Resource(object):

    def __init__(self, resource_id, name="", ema_values={}):
        self._resource_id = resource_id
        self._name = name
        self._ema_values = ema_values

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

    def add_sample(self, meter, value):
        print("add sample for meter {0} with value {1}".format(meter, value))
        if meter in self._ema_values.keys():
            ema_value = ema(value, self.ema_values[meter])
            self._ema_values[meter] = ema_value
        else:
            self._ema_values[meter] = value

        print("ema value: {0}".format(ema_value))

    def get_ema(self, meter):
        print("Getting ema value")
        if meter in self._ema_values.keys():
            return self._ema_values[meter]
        else:
            return None