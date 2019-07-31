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


def read_json_schemas(schema_dir):
    
    '''
    Reads json schemas from the directory provided
    '''
    
    schema = OrderedDict()
    for file in os.listdir(schema_dir):
        if not re.match(r'^.+.json$', file):
            continue

        with open(os.path.join(schema_dir, file), 'r') as f:
            schema_data = f.read()
        schema[file.rsplit('.', 1)[0]] = json.loads(schema_data)
    return schema


