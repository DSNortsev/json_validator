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


def pre_check(args):
    if args.filemode:
        if not os.path.isdir(filemode_dir):
            print('{}: directory does not exist'.format(filemode_dir))
            sys.exit(1)

        if len(os.listdir(filemode_dir)) == 0:
            print('{}: directory is empty'.format(filemode_dir))
            sys.exit(1)
    else:
        if not os.path.exists(log_file):
            print('{}: Log file does not exist'.format(log_file))
            sys.exit(1)

def read_logs(args):

    ''' Parse json messages from the log file or local files '''

    filtered_data = list()
    pre_check(args)

    if args.filemode:
        for file in os.listdir(filemode_dir):
            with open(os.path.join(filemode_dir, file), 'r') as f:
                filtered_data.append(f.read())
    else:
        with open(log_file, 'r') as f:
            raw_logs = f.read()
        filtered_data = re.findall(r'(?<=JSON: ).*', raw_logs)
    return filtered_data


def validate_json(filtered_data, all_schemas):

    ''' Iterate over json messages and validate against existing schema '''

    result = OrderedDict(success=0, fail=0, exceptions=0, message_processed=OrderedDict())
    message_processed = OrderedDict()
    error_count = 0
    log_output = OrderedDict()
    for js in filtered_data:
        try:
            data = json.loads(js)
        except:
            result['exceptions'] += 1
            continue

        message_type = data['header']['message_type']
        if message_type not in all_schemas.keys():
            continue

        if message_type not in message_processed.keys():
            message_processed[message_type] = 0

        try:
            validate(data, all_schemas[message_type])
            result['success'] += 1
        except jsonschema.exceptions.ValidationError as e:
            error_count += 1
            error_info = OrderedDict(title='Failed validating \'{}\' in schema{}'.format(e.validator,
                                                                                  list(e.relative_schema_path)[:-1]),
                              message_type=message_type,
                              message=e.message,
                              schema=e.schema,
                              instance=e.instance)
            log_output['error_message_{}'.format(error_count)] = OrderedDict(decription=error_info)
            result['fail'] += 1
        message_processed[message_type] += 1
    result['message_processed'] =  message_processed   
    log_output['result'] = result
    return log_output


def write_result_to_file(output_file, log_output):
    
    ''' Write result to log file '''
    
    with open(output_file, 'w') as f:
        json.dump(log_output, f, indent=4)

