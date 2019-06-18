# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 14:39:05 2019

@author: Rem
"""

import os
import json
from ibm_watson import DiscoveryV1

discovery = DiscoveryV1(
    version="1.0",
    iam_apikey="vr2KB1quF3UlOfmXAOvhfhXPv0ilmTKiCY0lsGQPrlTY",
    url="https://gateway-lon.watsonplatform.net/discovery/api"
)

with open(os.path.join(os.getcwd(), 'fwdcvs', 'sample.html')) as fileinfo:
    print(json.dumps(discovery.test_configuration_in_environment(environment_id='5f7b4d53-0b49-4c1e-a359-569b2775015f', configuration_id='43d58c94-1bbf-4142-873c-626319c91f21', file=fileinfo).get_result(), indent=2))