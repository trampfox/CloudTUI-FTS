__author__ = 'Davide Monfrecola'

from managers.manager import Manager

class NimbusManager (Manager):

    def __init__(self):
        print("Instance of class", NimbusManager.__name__)

    def check(self):
        print("Checking nimbus...")
        print("Done")
        pass
