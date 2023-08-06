'''
Extended implementation with records as JSON data.

Copyright 2022 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

import json

from .core import DaoDB

def json_from_binary(data):
    return json.loads(data.decode('utf-8'))

def json_to_binary(data):
    return json.dumps(data, ensure_ascii=False).encode('utf-8')

class JsonMixin:
    '''
    JSON coverter mix-in.
    '''

    def load_record(self, data_file, pos, size):
        data = super().load_record(data_file, pos, size)
        return json_from_binary(data)

    def append(self, data):
        data = json_to_binary(data)
        return super().append(data)

class JsonDaoDB(JsonMixin, DaoDB):
    pass
