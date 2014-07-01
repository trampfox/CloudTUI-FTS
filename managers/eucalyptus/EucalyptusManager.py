__author__ = 'Davide Monfrecola'

import boto
import os
from managers.manager import Manager
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import SubdomainCallingFormat
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.ec2.regioninfo import RegionInfo
from confmanager.eucalyptusconfmanager import EucalyptusConfManager

class EucalyptusManager(Manager):

    def __init__(self):
        self.conf = EucalyptusConfManager()
        self.conf.read()
        self.images = None
        self.security_groups = None
        self.keys = None
        self.snapshots = None
        self.volumes = None

    def connect(self):
        """Connection to the endpoint specified in the configuration file"""
        try:
            self.region = RegionInfo(name="eucalyptus", endpoint=self.conf.ec2_host)
            # trying connection to endpoint
            self.ec2conn = boto.connect_euca(host=self.conf.ec2_host,
                                             aws_access_key_id=self.conf.ec2_access_key_id,
                                             aws_secret_access_key=self.conf.ec2_secret_access_key,
                                             is_secure=False,
                                             port=int(self.conf.ec2_port),
                                             path=self.conf.ec2_path)

            #cf = OrdinaryCallingFormat()
            cf = SubdomainCallingFormat()

            self.s3conn = S3Connection(self.conf.ec2_access_key_id,
                                       self.conf.ec2_secret_access_key,
                                       host=self.conf.s3_host,
                                       port=int(self.conf.s3_port),
                                       path=self.conf.s3_path,
                                       is_secure=False,
                                       calling_format=cf)

            print("Connection successfully established")
            print("Connection successfully established (s3conn): " + self.s3conn.host)
        except Exception as e:
            print("Connection error({0})".format(e.message))

    """def get_all_configurations(self):
        self.instance_types = self.ec2conn.get_all_instance_types()
        self.security_groups = self.ec2conn.get_all_security_groups()
        self.key_pairs = self.ec2conn.get_all_key_pairs()
        self.images = self.ec2conn.get_all_images()"""

    def show_menu(self):
        os.system("clear")
        menu_text = """\nWhat would you like to do?
--------------------------
1) Create new instance
2) Show running instances
3) Stop/pause/reboot instance
4) Create new volume
5) Show available volumes
6) Show key pairs
7) Show connection information
8) Exit\n"""
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
                self.terminate_vm()
            else:
                raise Exception("Unavailable choice!")
        except Exception as e:
            print(e.message)

    def create_new_instance(self):
        """

        :return:
        """
        self.print_all_images()
        image_index = input("Select image: ")
        image_id = self.images[image_index - 1].id
        self.print_all_instance_types()
        instance_type_index = input("Select instance type: ")
        instance_type = self.instance_types[instance_type_index - 1].name
        self.print_all_security_groups()
        security_group_index = input("Select security group: ")
        security_group = self.security_groups[security_group_index - 1].name
        self.print_all_key_pairs()
        key_pair_index = input("Select key pair: ")
        key_name = self.key_pairs[key_pair_index - 1].name

        print("\nCreating new instance with the following properties:")
        print("-- Image ID: " + str(image_id))
        print("-- Instance type: " + str(instance_type))
        print("-- Security group: " + str(security_group))
        print("-- Key pair: " + str(key_name))
        #print("\nDo you want to continue? (y/n)")

        try:
            reservation = self.ec2conn.run_instances(image_id=image_id,
                                                     key_name=key_name,
                                                     instance_type=instance_type,
                                                     security_groups=[security_group],
                                                     min_count=1,
                                                     max_count=1)
            print reservation
        except Exception as e:
            print("An error occured: {0}".format(e.message))

