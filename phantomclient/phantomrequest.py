__author__ = 'Davide Monfrecola'

import requests
import json
from requests.auth import HTTPBasicAuth

class PhantomRequest():

    def __init__(self):
        pass

    def auth(self):
        pass

    def test(self):
        pass
        #r = requests.get('https://phantom.nimbusproject.org/api/dev/sites',
        #                 headers={'Authorization': 'Basic %s' % self.basic_auth})
        #print r.text