from Queue import Queue
import logging
from threading import Thread
from managers.openstack.openstackagent import OpenstackAgent
from monitors.openstackmonitor import OpenstackMonitor
from rules.ruleengine import RuleEngine

__author__ = 'Davide Monfrecola'

from confmanager.openstackconfmanager import OpenstackConfManager
from novaclient.client import Client

class OpenstackManager:

    def __init__(self):
        self.conf = OpenstackConfManager()
        self.conf.read()
        self.images = None
        self.instance_types = None
        self.keys = None
        self.security_groups = None
        self.networks = None
        self.instances = None
        self.os_monitor = None
        self.rule_engine_monitor = None
        self.os_agent = None
        self.os_monitor = None

    def get_conf(self):
        return self.conf

    def connect(self):
        """Connection to the endpoint specified in the configuration file"""
        # OpenStack Python SDK #
        try:
            self.nova = Client(2,
                               self.conf.username,
                               self.conf.password,
                               self.conf.tenant_name,
                               self.conf.auth_url)

            logging.debug("Client instance successfully created")
        except Exception as e:
            logging.error("Connection error({0})".format(e.message))

        # end OpenStack Python SDK #

    def create_new_instance(self):

        # image
        self.print_all_images()
        if len(self.images) > 0:
            image_index = input("Select image: ")
            self.image = self.images[image_index - 1]._info['name']
        else:
            print("There are no images available!")
            return False
        #flavor
        self.print_all_instance_types()
        if len(self.instance_types) > 0:
            instance_index = input("Select instance type: ")
            self.instance_type = self.instance_types[instance_index - 1]._info['name']
        else:
            print("There are no instance types available!")
            return False
        # security groups
        self.print_all_security_groups()
        if len(self.security_groups) > 0:
            security_group_index = input("Select security group: ")
            self.security_group = self.security_groups[security_group_index - 1].name
        else:
            print("There are no security groups available!")
            return False
        # key name
        self.print_all_networks()
        if len(self.networks) > 0:
            key_index = input("Select network: ")
            self.network = self.networks[key_index - 1].label
            self.network_id = self.networks[key_index - 1].id
        else:
            print("There are no networks available!")
            return False
        # network
        self.print_all_key_pairs()
        if len(self.keys) > 0:
            key_index = input("Select key: ")
            self.key_name = self.keys[key_index - 1]._info['keypair']['name']
        else:
            print("There are no keys available!")
            return False

        server_name = raw_input("Insert instance name: ")

        print("\n--- Creating new instance with the following properties:")
        print("- %-20s %-30s" % ("Image name", str(self.image)))
        print("- %-20s %-30s" % ("Instance type", str(self.instance_type)))
        print("- %-20s %-30s" % ("Security group", str(self.security_group)))
        print("- %-20s %-30s" % ("Key pair", str(self.key_name)))
        print("- %-20s %-30s" % ("Network", str(self.network)))

        image = self.nova.images.find(name=self.image)
        flavor = self.nova.flavors.find(name=self.instance_type)
        nics = [{"net-id": self.network_id}]

        instance = self.nova.servers.create(name=server_name,
                                            image=image,
                                            flavor=flavor,
                                            key_name=self.key_name,
                                            security_groups=[self.security_group],
                                            nics=nics)

    def instance_action(self, action):
        try:
            self.print_all_instances()
            if len(self.instances) == 0:
                print("You don't have any instance running or pending")
            else:
                instance_index = input("Please select the instance: ")

            if action == "reboot":
                self.nova.servers.reboot(self.instances[instance_index - 1])
                print("Instance rebooted")
            elif action == "delete":
                self.nova.servers.delete(self.instances[instance_index - 1])
                print("Instance terminated")
            elif action == "diagnostic":
                diagnostics = self.nova.servers.diagnostics(self.instances[instance_index - 1])
                print(diagnostics)
            else:
                raise Exception("Action not supported")

        except Exception as e:
            print("An error occured: {0}".format(e.message))

    def get_instance_info(self):
        info = []
        for instance in self.nova.servers.list():
            info.append({"id": instance.id, "name": instance.name})

        return info

    def print_all_instances(self):
        """Print instance id, image id, public DNS and state for each active instance"""
        print("--- Instances ---")
        print("%-10s %-25s %-25s %-25s %-70s %-20s" % ("-", "Name", "Created", "Key name", "Private IP Address", "Status"))
        self.instances = self.nova.servers.list()

        if len(self.instances) == 0:
            print("You don't have any instance running or pending")
        else:
            i = 1
            for instance in self.instances:
                print("%-10s %-25s %-25s %-25s %-70s %-20s" % (i, instance.name, instance._info['created'],
                                                               instance._info['key_name'], instance.networks,
                                                               instance.status))
                i += 1

    def clone_instance(self, instance_id):
        '''
        Create a new instance that is a clone of the instance with the instance ID
        passed as parameter
        '''
        instance = self.nova.servers.get(instance_id)

        if self.networks is None:
            self.networks = self.nova.networks.list()

        nics = []
        for net_id in instance._info['addresses'].keys():
            for network in self.networks:
                if network.label == net_id:
                    nics.append({"net-id": network.id})

        security_groups = []
        for security_group in instance._info['security_groups']:
            security_groups.append(security_group['name'])

        print("")
        print("*" * 80)
        print("Cloning the instance {0}...".format(instance_id))
        print("name: " + instance.name + "-clone")
        print("image id: " + str(instance._info['image']['id']))
        print("flavor id: " + str(instance._info['flavor']['id']))
        print("key name: " + str(instance._info['key_name']))
        print("sec groups: " + str(security_groups))
        print("nics: " + str(nics))
        print("*" * 80)
        print("")

        instance = self.nova.servers.create(name=instance.name + "-clone",
                                            image=instance._info['image']['id'],
                                            flavor=instance._info['flavor']['id'],
                                            key_name=instance._info['key_name'],
                                            security_groups=security_groups,
                                            nics=nics)

    def print_all_images(self):
        """
        Print id and other useful information of all images available
        """
        print("--- Images available ---")
        print("%-10s %-40s %-55s %-25s" % ("ID", "Image ID", "Name", "State"))
        if self.images is None:
            self.images = self.nova.images.list()
        i = 1
        for image in self.images:
            print("%-10s %-40s %-55s %-25s" % (i, image._info['id'], image._info['name'], image._info['status']))
            i = i + 1

    def print_all_instance_types(self):
        """
        Print id and other useful information of all instance types available
        """
        print("--- Instance type available ---")
        print("%-10s %-25s %-15s %-15s %-15s" % ("ID", "Instance name", "Memory (MB)", "Disk (GB)", "Cores"))
        if self.instance_types is None:
            self.instance_types = self.nova.flavors.list()

        for instance_type in self.instance_types:
            print("%-10s %-25s %-15s %-15s %-15s" % (instance_type._info['id'], instance_type._info['name'],
                                                     instance_type._info['ram'], instance_type._info['disk'],
                                                     instance_type._info['vcpus']))

    def print_all_key_pairs(self):
        """
        Print id and other useful information of all key pairs available
        """
        print("--- Keys available ---")
        print("%-10s %-25s %-35s" % ("ID", "Key name", "Key fingerprint"))
        if self.keys is None:
            self.keys = self.nova.keypairs.list()
        i = 1
        for key in self.keys:
            print("%-10s %-25s %-35s" % (i, key._info['keypair']['name'], key._info['keypair']['fingerprint']))
            i = i + 1

    def print_all_security_groups(self):
        """
        Print id and other useful information of all security groups available
        """
        print("--- Security groups available ---")
        print("%-10s %-25s %-35s" % ("ID", "SG name", "SG description"))
        if self.security_groups is None:
            self.security_groups = self.nova.security_groups.list()
        i = 1
        for security_group in self.security_groups:
            print("%-10s %-25s %-35s" % (i, security_group.name, security_group.description))
            i = i + 1

    def print_all_networks(self):
        """
        Print id and other useful information of all networks available
        """
        print("--- Networks available ---")
        print("%-10s %-25s %-35s" % ("ID", "Network name", "Description"))
        if self.networks is None:
            self.networks = self.nova.networks.list()
        i = 1
        print(self.networks[0])
        for network in self.networks:
            print("%-10s %-25s %-30s" % (i, network.label, network.id))
            i = i + 1

    def monitor_status(self):
        if self.os_monitor is not None:
            print("Monitor enabled\n")
            self.print_monitored_instances()
        else:
            print("Monitor not enabled\n")

    def print_monitored_instances(self):
        pass

    def start_stop_monitor(self):
        if self.os_monitor is not None:
            self.stop_monitor()
            print("Openstack monitor agent has been stopped")
        else:
            logging.debug("Monitor not enabled, starting threads")
            print("Starting Openstack monitor...")
            self.start_monitor()

    def start_monitor(self):
        meters_queue = Queue()
        cmd_queue = Queue()

        resources = self.get_instance_info()
        self.os_monitor = OpenstackMonitor(resources=resources, conf=self.conf)
        monitor = Thread(target=self.os_monitor.run, args=(meters_queue,))
        monitor.setDaemon(True)
        monitor.start()
        logging.info("OpenstackMonitor thread started")

        rule_engine = RuleEngine(resources=resources, cmd_queue=cmd_queue)
        self.rule_engine_monitor = Thread(target=rule_engine.run, args=(meters_queue,))
        self.rule_engine_monitor.setDaemon(True)
        self.rule_engine_monitor.start()
        logging.info("RuleEngine thread started")

        agent = OpenstackAgent(manager=self)
        self.os_agent = Thread(target=agent.run, args=(cmd_queue,))
        self.os_agent.setDaemon(True)
        self.os_agent.start()
        logging.info("OpenstackAgent thread started")
        # cmd_queue.put({'command': 'stop'})

    def stop_monitor(self):
        logging.debug("Monitor enabled, stopping threads")
        self.os_monitor.stop()
        self.rule_engine_monitor.stop()
        self.os_agent.stop()
        logging.info("Monitor agents have been stopped")

    def show_menu(self):
        menu_text = """\nWhat would you like to do?
--------------------------
1) Create new instance
2) Show running instances
3) Reboot instance
4) Terminate instance
5) Retrieve diagnostic
6) Start/stop monitor
7) Monitor status
8) Exit
\n"""
        print(menu_text)

        logging.info("CloudTUI-fts Openstack manager started")

        try:
            # user input
            print("Please make a choice: ")
            choice = input()
            if choice == 1:
                self.create_new_instance()
            elif choice == 2:
                self.print_all_instances()
            elif choice == 3:
                self.instance_action("reboot")
            elif choice == 4:
                self.instance_action("delete")
            elif choice == 5:
                self.instance_action("diagnostic")
            elif choice == 6:
                self.start_stop_monitor()
            elif choice == 7:
                self.monitor_status()
            elif choice == 8:
                 exit(0)
            else:
                raise Exception("Unavailable choice!")
        except Exception as e:
            print(e.message)
