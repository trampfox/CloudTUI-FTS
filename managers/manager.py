__author__ = 'Davide Monfrecola'

import boto
import os
import base64
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.ec2.regioninfo import RegionInfo
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType
from imanager import IManager

class Manager(IManager):
    """Common base class for all cloud platform manager (implements IManager interface)"""

    def __init__(self):
        self.running_instances = []

    def connect(self):
        # trying connection to endpoint. self.region and self.conf are initialized in subclasses (e.g.: NimbusManager)
        self.ec2conn = boto.connect_ec2(self.conf.ec2_access_key_id,
                                        self.conf.ec2_secret_access_key,
                                        region=self.region,
                                        port=self.conf.port,
                                        path=self.conf.ec2_path,
                                        is_secure=False)

        cf = OrdinaryCallingFormat()

        self.s3conn = S3Connection(self.conf.ec2_access_key_id,
                                   self.conf.ec2_secret_access_key,
                                   host=self.conf.s3_host,
                                   port=int(self.conf.s3_port),
                                   is_secure=False,
                                   calling_format=cf)

    def close_connections(self):
        self.ec2conn.close()
        self.s3conn.close()

    def get_instance(self, instance_index):
        instances = self.ec2conn.get_all_instances()
        if len(instances) == 0:
            return None
        else:
            return instances[0].instances[instance_index]

    def get_all_instance_ids(self):
        instances = self.ec2conn.get_all_instances()
        return [vm.id for instance in instances for vm in instance.instances]

    def print_all_instances(self):
        """Print instance id, image id, public DNS and state for each active instance"""
        print("Retrieving all instances...")
        instances = self.ec2conn.get_all_instances()
        instances_objects = [vm for instance in instances for vm in instance.instances]

        if len(instances_objects) == 0:
            print("You don't have any instance running or pending")
        else:
            i = 1
            for instance in instances_objects:
                print("{0} - Instance: {1} | DNS name: {2} | Status: {3}".format(i, instance.id + " / " + instance.image_id, instance.public_dns_name, instance.state))
                i += 1

    def print_all_volumes(self):
        """
        Print id and other useful information about all volumes
        """
        print("--- Volumes available ---")
        print("%-10s %-25s %-15s %-25s" % ("ID", "Volume ID", "Size (GB)", "Status"))
        if self.volumes is None:
            self.volumes = self.ec2conn.get_all_volumes()
        i = 1
        for volume in self.volumes:
            print("%-10s %-25s %-15s %-25s" % (i, volume.id, volume.size, volume.status))
            i = i + 1

    def print_all_security_groups(self):
        """
        Print id and other useful information about all security groups
        """
        print("--- Security groups available ---")
        print("%-10s %-25s %-35s" % ("ID", "SG name", "SG description"))
        if self.security_groups is None:
            self.security_groups = self.ec2conn.get_all_security_groups()
        i = 1
        for security_group in self.security_groups:
            print("%-10s %-25s %-35s" % (i, security_group.name, security_group.description))
            i = i + 1

    def print_all_zones(self):
        """
        Print id and other useful information about all zones
        """
        print("--- Zones available ---")
        print("%-10s %-25s %-35s" % ("ID", "Zone name", "Zone state"))
        if self.zones is None:
            self.zones = self.ec2conn.get_all_zones()
        i = 1
        for zone in self.zones:
            print("%-10s %-25s %-35s" % (i, zone.name, zone.state))
            i = i + 1

    def print_all_instance_types(self):
        """
        Print id and other useful information about all instance types
        """
        print("--- Instance type available ---")
        print("%-10s %-25s %-15s %-15s %-15s" % ("ID", "Instance name", "Memory (MB)", "Disk (GB)", "Cores"))
        if self.instance_types is None:
            self.instance_types = self.ec2conn.get_all_instance_types()
        i = 1
        for instance_type in self.instance_types:
            print("%-10s %-25s %-15s %-15s %-15s"%(i, instance_type.name, instance_type.memory,
                                                   instance_type.disk, instance_type.cores))
            i = i + 1

    def print_all_key_pairs(self):
        """
        Print id and other useful information about all instance types
        """
        print("--- Keys available ---")
        print("%-10s %-25s %-35s" % ("ID", "Key name", "Key fingerprint"))
        if self.keys is None:
            self.keys = self.ec2conn.get_all_key_pairs()
        i = 1
        for key in self.keys:
            print("%-10s %-25s %-35s" % (i, key.name, key.fingerprint))
            i = i + 1

    def print_all_images(self):
        """
        Print id and other useful information about all images
        """
        print("--- Images available ---")
        print("%-10s %-25s %-25s %-25s %-25s" % ("ID", "Image ID", "Kernel ID", "Type", "State"))
        if self.images is None:
            self.images = self.ec2conn.get_all_images()
        i = 1
        for image in self.images:
            print("%-10s %-25s %-25s %-25s %-25s" % (i, image.id, image.kernel_id, image.type, image.state))
            i = i + 1

    def print_all_snapshots(self):
        """
        Print id and other useful information about all images
        """
        print("--- Snapshots available ---")
        print("%-10s %-25s %-25s %-25s %-25s" % ("ID", "Image ID", "Kernel ID", "Type", "State"))
        if self.snapshots is None:
            self.snapshots = self.ec2conn.get_all_snapshots()
        i = 1
        for snapshot in snapshots:
            #print("%-10s %-25s %-25s %-25s %-25s" % (i, image.id, image.kernel_id, image.type, image.state))
            i = i + 1

    def create_new_instance(self):
        """

        :return:
        """
        # image
        self.print_all_images()
        if len(self.images) > 0:
            image_index = input("Select image: ")
            self.image_id = self.images[image_index - 1].id
        else:
            print("There are no images available!")
            return False
        # security group
        self.print_all_security_groups()
        if len(self.security_groups) > 0:
            security_group_index = input("Select security group: ")
            self.security_group = [self.security_groups[security_group_index - 1].name]
        else:
            self.security_group = None
            print("There are no security groups available!")
        # key name
        self.print_all_key_pairs()
        if len(self.keys) > 0:
            key_pair_index = input("Select key pair: ")
            self.key_name = self.keys[key_pair_index - 1].name
        else:
            self.key_name = None
            print("There are no keys available!")

    def terminate_instance(self):
        ids = self.get_all_instance_ids()

        if len(ids) == 0:
            print("You don't have any instance running or pending")
        else:
            try:
                self.print_all_instances()
                print("0 - Cancel")
                print("")
                vm_index = input("Please select the VM that you want to terminate: ")
                # terminate selected vm
                print("Selected: " + str([ids[vm_index - 1]]))
                self.ec2conn.terminate_instances(instance_ids=[ids[vm_index - 1]])
                print("Instance terminated")
            except Exception as e:
                print("An error occured: {0}".format(e.message))

    def reboot_instance(self):
        ids = self.get_all_instance_ids()

        if len(ids) == 0:
            print("You don't have any instance running or pending")
        else:
            try:
                self.print_all_instances()
                print("0 - Cancel")
                print("")
                vm_index = input("Please select the VM that you want to reboot: ")
                # terminate selected vm
                print("Selected: " + str([ids[vm_index - 1]]))
                self.ec2conn.reboot_instances(instance_ids=[ids[vm_index - 1]])
                print("Instance rebooted")
            except Exception as e:
                print("An error occured: {0}".format(e.message))