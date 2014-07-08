__author__ = 'Davide Monfrecola'

import boto
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.ec2.regioninfo import RegionInfo
from managers.manager import Manager
from confmanager.openstackconfmanager import OpenStackConfManager
import novaclient.v1_1.client as nvclient

class OpenStackManager():
    
    def __init__(self):
        self.conf = OpenStackConfManager()
        self.conf.read()
        self.images = None
        self.instance_types = None
        self.keys = None
        self.security_groups = None
        self.networks = None

    def connect(self):
        """Connection to the endpoint specified in the configuration file"""
        """try:
            # boto #
            self.region = RegionInfo(name="nova", endpoint=self.conf.ec2_host)
            # trying connection to endpoint
            Manager.connect(self)
            # end boto #

            print("Connection successfully established")
            print("Connection successfully established (s3conn): " + self.s3conn.host)
        except Exception as e:
            print("Connection error({0})".format(e.message))"""

        # OpenStack Python SDK #
        try:
            self.nova = nvclient.Client(auth_url=self.conf.auth_url,
                                        username=self.conf.username,
                                        api_key=self.conf.api_key,
                                        project_id=self.conf.tenant_name,
                                        insecure=True)

            print("Connection successfully established ")
            #print("Connection successfully established (s3conn): " + self.s3conn.host)
        except Exception as e:
            print("Connection error({0})".format(e.message))

        # end OpenStack Python SDK #

    def create_new_instance(self):
        image = self.nova.images.find(name="futuregrid/ubuntu-14.04")
        flavor = self.nova.flavors.find(name="m1.tiny")

        instance = self.nova.servers.create(name="vm2", image=image,
                                            flavor=flavor, key_name="trampfox-key")

    def print_all_instances(self):
        """Print instance id, image id, public DNS and state for each active instance"""
        print("--- Instances ---")
        print("%-10s %-25s %-25s %-25s %-25s %-20s" % ("-", "Name", "Created", "Key name", "Private IP Address", "Status"))
        instances = self.nova.servers.list()

        if len(instances) == 0:
            print("You don't have any instance running or pending")
        else:
            i = 1
            for instance in instances:
                print("%-10s %-25s %-25s %-25s %-25s %-20s" % (i, instance.name, instance._info['created'],
                                                               instance._info['key_name'], instance.networks['private'],
                                                               instance.status))
                i += 1

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
        print("%-10s %-25s %-35s" % ("ID", "Network name", ""))
        if self.networks is None:
            self.networks = self.nova.networks.list()
        i = 1
        for network in self.networks:
            print("%-10s %-25s %-35s" % (i, network.name, network.description))
            i = i + 1

    def show_menu(self):
        menu_text = """\nWhat would you like to do?
--------------------------
1) Create new instance
2) Show running instances
3) Reboot instance
4) Terminate instance
5) Exit\n"""
        print(menu_text)
        try:
            # user input
            print("Please make a choice: ")
            choice = input()
            if choice == 1:
                self.create_new_instance()
            elif choice == 2:
                self.print_all_instances()
            elif choice == 3:
                self.print_all_instance_types()
            elif choice == 4:
                self.print_all_key_pairs()
            elif choice == 5:
                self.print_all_security_groups()
            elif choice == 6:
                self.print_all_networks()
            else:
                raise Exception("Unavailable choice!")
        except Exception as e:
            print(e.message)