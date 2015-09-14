from managers.eucalyptus.eucalyptusmanager import EucalyptusManager
from managers.nimbus.nimbusmanager import NimbusManager
from managers.openstack.openstackmanager import OpenstackManager

__author__ = 'Davide Monfrecola'


class CloudTUI:

    def __init__(self):
        pass

    def start(self):
        constructor = self.show_menu()
        # Create a new instance according to user platform selection
        manager = constructor()
        manager.connect()

        while(True):
            manager.show_menu()

    def show_menu(self):
        global kill

        print("CloudTUI-fts")
        print("Please select the Cloud platform that you want to use:")

        print("1) OpenStack")
        print("2) Nimbus")
        print("3) Eucalyptus")

        while True:
            try:
                # user input
                print("Please make a choice: ")
                choice = input()
                constructor = self.get_constructor(choice)
                break
            except Exception:
                print("Unavailable choice!")

        return constructor

    def get_constructor(self, platform):
      return {
        3: NimbusManager,
        2: EucalyptusManager,
        1: OpenstackManager
      }[platform]