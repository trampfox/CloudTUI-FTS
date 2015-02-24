__author__ = 'Davide Monfrecola'


class Resource(object):

    def __init__(self, resource_id, ewma_values={}):
        self.resource_id = resource_id
        self.ewma_values = ewma_values

        print "created an instance of Resource (id: {0})".format(self.resource_id)

    @property
    def resource_id(self):
        return self._resource_id

    def set_ewma(self, meter, value):
        self.ewma_values[meter] = value

    def get_ewma(self, meter):
        if meter in self.ewma_values.keys():
            return self.ewma_values[meter]
        else:
            return None