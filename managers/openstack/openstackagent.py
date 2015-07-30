__author__ = 'Davide Monfrecola'

import logging

class OpenstackAgent:

    def __init__(self, manager):
        self.manager = manager
        #self.manager.connect()
        self.signal = True

    def run(self, cmd_queue):
        while self.signal:
            try:
                command = cmd_queue.get()
                print("[Openstack agent] Command received: " + str(command))

                self.execute_command(command)
            except Exception, e:
                print("Error %s:" % e.args[0])

    def set_stop_signal(self, command):
        print("[Openstack agent] Set signal to False")
        self.signal = False

    def get_action_method(self, action):
        return {
            'clone': self.manager.clone_instance,
            'stop': self.set_stop_signal
        }[action]

    def execute_command(self, command):
        action_method = self.get_action_method(command['command'])
        action_method(command)
