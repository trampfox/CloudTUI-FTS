__author__ = 'Davide Monfrecola'

import logging

class OpenstackAgent:

    def __init__(self, manager):
        self.manager = manager
        self.signal = True

    def run(self, cmd_queue):
        while self.signal:
            try:
                command = cmd_queue.get()
                logging.debug("Command received: " + str(command))

                self.execute_command(command)
            except Exception, e:
                logging.error("Error %s:" % e.args[0])
                print("An error occured. Please see logs for more information")

    def set_stop_signal(self):
        logging.debug("Set signal to False")
        self.signal = False

    def get_action_method(self, action):
        return {
            'clone': self.manager.clone_instance,
            'stop': self.set_stop_signal
        }[action]

    def execute_command(self, command):
        logging.debug("Executing command {0}".format(command))
        action_method = self.get_action_method(command['command'])
        action_method(command['resource_id'])

    def stop(self):
        self.set_stop_signal()