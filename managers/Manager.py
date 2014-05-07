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
        print("Instance of class", Manager.__name__)

    def connect(self):
        # trying connection to endpoint. self.region and self.conf are initialized in subclasses (e.g.: NimbusManager)
        self.ec2conn = boto.connect_ec2(self.conf.vws_repository_s3id, self.conf.vws_repository_s3key,
                                        region=self.region, port=self.conf.port)
        cf = OrdinaryCallingFormat()

        self.s3conn = S3Connection(self.conf.vws_repository_s3id, self.conf.vws_repository_s3key,
                                   host=self.conf.vws_repository_host, port=int(self.conf.vws_repository_port),
                                   is_secure=False, calling_format=cf)

    def close_connections(self):
        self.ec2conn.close()
        self.s3conn.close()

    def get_all_instances(self):
        return self.ec2conn.get_all_instances()

    def get_all_instance_ids(self):
        instances = self.ec2conn.get_all_instances()

        ids = []

        if len(instances) == 0:
            print("You don't have any instance running or pending")
        else:
             for instance in instances:
                for vm in instance.instances:
                    ids.append(vm.id)

        return ids

    def get_instance(self, instance_index):
        instances = self.ec2conn.get_all_instances()
        if len(instances) == 0:
            return None
        else:
            return instances[0].instances[instance_index]


    def print_all_instances(self):
        """Print instance id, image id, public DNS and state for each active instance"""
        instances = self.ec2conn.get_all_instances()

        if len(instances) == 0:
            print("You don't have any instance running or pending")
        else:
            for instance in instances:
                i = 1
                for vm in instance.instances:
                    print("{0} - Instance: {1} | DNS name: {2} | Status: {3}".format(i, vm.id + " / " + vm.image_id, vm.public_dns_name, vm.state))

    def terminate_vm(self):
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