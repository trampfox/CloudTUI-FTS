__author__ = 'Davide Monfrecola'

class IManager:
    """This interface defines all the methods that a cloud platform manager class must implement """

    def __init__(self):
        pass

    def connect(self): raise NotImplementedError

    def close_connections(self): raise NotImplementedError

    def get_all_instances(self): raise NotImplementedError

    def print_all_instances(self): raise NotImplementedError

    def login_vm(self): raise NotImplementedError

    def run_vm(self): raise NotImplementedError

    def clone_instance(self, instance): raise NotImplementedError

    def terminate_vm(self): raise NotImplementedError