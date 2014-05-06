__author__ = 'Davide Monfrecola'

import json
from managers.nimbus.nimbusmanager import NimbusManager

class CloudTUI:

    def __init__(self):
        pass

    def start(self):
        platform_selected = self.show_menu()
        # Create a new instance according to user platform selection
        constructor = globals()[str(platform_selected[1])]
        instance = constructor()

        instance.connect()
        instance.terminate_vm()

    def show_menu(self):
        global kill

        print("CloudTUI-advance")
        print("Please select the Cloud platform that you want to use:")

        try:
            with open("platforms.txt", "r") as platforms_file:
                content = platforms_file.read()
        except IOError:
            print("Bad platforms configuration file. Program Terminated.")
            kill = True
            exit()
        # load available platforms from json config file
        platform_available = json.loads(content)

        i = 1
        # show available platforms
        for (platform_name, platform_manager) in platform_available.items():
            print(str(i) + ") " + platform_name)
            i += 1

        while True:
            try:
                # user input
                print("Please make a choice: ")
                choice = input()
                platform_selected = platform_available.items()[choice - 1]
                break
            except Exception:
                print("Unavailable choice!")


        return platform_selected