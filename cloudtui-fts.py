#!/usr/bin/python
__author__ = 'Davide Monfrecola'

import sys
import logging

from cloudtui.cloudtui import CloudTUI


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":

    logging.basicConfig(filename='logs/cloudtui-fts.log',
                        format="%(levelname)s::%(asctime)s - %(module)s(line %(lineno)d) : %(message)s",
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG,
                        filemode='a')

    cloudTUI = CloudTUI()
    cloudTUI.start()
'''
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
'''
