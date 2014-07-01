__author__ = 'Davide Monfrecola'

import boto
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.ec2.regioninfo import RegionInfo
from managers.manager import Manager
from confmanager.nimbusconfmanager import NimbusConfManager

class NimbusManager (Manager):

    def __init__(self):
        self.conf = NimbusConfManager()
        self.conf.read()
        self.conf.read_cloud_conf()

    def connect(self):
        """Connection to the endpoint specified in the configuration file"""
        try:
            self.region = RegionInfo(name="nimbus", endpoint=self.conf.ec2_host)
            # trying connection to endpoint
            Manager.connect(self)

            print("Connection successfully established: " + self.ec2conn.host)
            print("Connection successfully established (s3conn): " + self.s3conn.host)
        except Exception as e:
            print("Connection error({0})".format(e.message))

    def clone_instance(self, instance):
        print("Clone start")
        cf = OrdinaryCallingFormat()

        # get all buckets that user owns
        try:
            buckets = self.s3conn.get_bucket("Repo", validate=False)
        except:
            raise
        # test
        print buckets

    def run_vm(self):

        images = self.ec2conn.get_all_images()
        image_ids = []

        try:
            print("-- Available images --")
            i = 1
            for image in images:
                print("{0}) {1} - {2} - {3} - {4}").format(i, image.id, image.kernel_id, image.type, image.state)
                image_ids.append(image.id)
                i = i + 1

            choice = input("Please select the image to run (0 return to main manu): ")

            if int(choice) == 0:
                return 0;
            else:
                selected_vm_id = image_ids[choice - 1]

            print("Creating new instance for image {0}").format(selected_vm_id)

            self.ec2conn.run_instances(selected_vm_id, min_count=1, max_count=1, instance_type="m1.medium")

        except Exception as e:
            print("An error occured: {0}").format(e.message)

    # def clone_instance(self, instance):
    #     """
    #     Make an clone of an existing Instance object.
    #
    #     instance      The Instance object to clone.
    #     """
    #
    #     # TO DO -> the instance selection should be outside of this method
    #     self.print_all_instances()
    #     print("")
    #     vm_index = input("Please select the VM that you want to clone: ")
    #     instance = self.get_instance(vm_index - 1)
    #
    #     new_bdm = None
    #     ec2 = instance.connection
    #     user_data = None
    #
    #     if instance.block_device_mapping:
    #         root_device_name = instance.get_attribute('rootDeviceName')['rootDeviceName']
    #         user_data = instance.get_attribute('userData')['userData']
    #         # user_data comes back base64 encoded.  Need to decode it so it
    #         # can get re-encoded by run_instance !
    #         user_data = base64.b64decode(user_data)
    #         new_bdm = BlockDeviceMapping()
    #
    #         for dev in instance.block_device_mapping:
    #             # if this entry is about the root device, skip it
    #             if dev != root_device_name:
    #                 bdt = instance.block_device_mapping[dev]
    #                 if bdt.volume_id:
    #                     volume = ec2.get_all_volumes([bdt.volume_id])[0]
    #                     snaps = volume.snapshots()
    #                     if len(snaps) == 0:
    #                         print 'No snapshots available for %s' % volume.id
    #                     else:
    #                         # sort the list of snapshots, newest is at the end now
    #                         snaps.sort(key=lambda snap: snap.start_time)
    #                         latest_snap = snaps[-1]
    #                         new_bdt = BlockDeviceType()
    #                         new_bdt.snapshot_id = latest_snap.id
    #                         new_bdm[dev] = new_bdt
    #
    #     return ec2.run_instances(instance.image_id,
    #                              key_name=instance.key_name,
    #                              security_groups=[g.name for g in instance.groups],
    #                              user_data=user_data,
    #                              instance_type=instance.instance_type,
    #                              kernel_id=instance.kernel,
    #                              ramdisk_id=instance.ramdisk,
    #                              monitoring_enabled=instance.monitored,
    #                              placement=instance.placement,
    #                              block_device_map=new_bdm).instances[0]