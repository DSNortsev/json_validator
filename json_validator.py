#! /usr/bin/env python3

import argparse
import os
import sys
import re
import json
from jsonschema import validate
import jsonschema
from collections import OrderedDict


name = os.path.basename(__file__).rsplit('.', 1)[0]
schema_dir = 'schemas/'
log_file = ''
json_dir = ""
output_file = f'{name}.out'


def usage():
    parser = argparse.ArgumentParser(description='Validate JSON data against a JSON schema ')
    parser.add_argument("-f", "--file", dest="filemode", default=False,
                        action="store_true",
                        help=f"Parse json messages from {json_dir}")

    parser.add_argument("-v", "--verbose",
                        dest="verbose", default=False, action="store_true",
                        help="Output all errors and warning on the screen")
    arguments = parser.parse_args()
    return arguments

