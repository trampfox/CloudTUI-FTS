__author__ = 'Davide Monfrecola'

from managers.Manager import Manager


class NimbusManager (Manager):

    def __init__(self):
        print("Instance of class", NimbusManager.__name__)

    def check(self):
        print("Checking Nimbus...")
        print("Done")
        pass
