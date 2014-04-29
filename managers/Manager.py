__author__ = 'Davide Monfrecola'

import IManager

class Manager(IManager):
    """Common base class for all cloud platform manager (implements IManager interface)"""

    def __init__(self):
        print("Instance of class", Manager.__name__)