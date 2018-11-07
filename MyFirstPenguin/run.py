from __future__ import print_function
import os
import json
import random
import math
import sys
from utilities import *
from movement import *
from eirik import *
from pprint import pprint
import time

"""
tactics:
* hvis en power up forsvinner vet vi hvor fienden er
* Try og except er bedre enn if-setninger, burde alltid prioriteres 
"""


env = os.environ
req_params_query = env['REQ_PARAMS_QUERY']
responseBody = open(env['res'], 'w')

response = {}
returnObject = {}
if req_params_query == "info":
    returnObject["name"] = "Pingu Noot Noot"
    returnObject["team"] = "Penguin Team Six1"
elif req_params_query == "command":    
    body = json.loads(open(env["req"], "r").read())
    print("------------------ NEW RESPONSE ------------------")
    print("Visibility: ", body['visibility'])
    returnObject["command"] = chooseAction(body)
    print("------------------ END RESPONSE ------------------")
    time.sleep(0.5)



response["body"] = returnObject
responseBody.write(json.dumps(response))
responseBody.close()


