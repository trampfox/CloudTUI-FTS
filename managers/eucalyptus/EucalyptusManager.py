__author__ = 'Davide Monfrecola'

from managers.manager import Manager

class EucalyptusManager(Manager):

    def __init__(self):
        print("Instance of class", EucalyptusManager.__name__)
