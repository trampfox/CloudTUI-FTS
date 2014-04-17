__author__ = 'Davide Monfrecola'

class Manager:
    """Common base class for all cloud platform manager"""

    def __init__(self):
        print("Instance of class", Manager.__name__)