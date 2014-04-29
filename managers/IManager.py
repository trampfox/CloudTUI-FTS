__author__ = 'Davide Monfrecola'

class IManager:
    """This interface defines all the methods that a cloud platform manager class must implement """

    def __init__(self):
        pass

    def show_instances(self): raise NotImplementedError