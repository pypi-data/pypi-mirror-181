'''
Snappy compression module.

Copyright 2022 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

import snappy

class SnappyMixin:
    '''
    Snappy compression mix-in.
    '''

    def load_record(self, data_file, pos, size):
        data = super().load_record(data_file, pos, size)
        return snappy.uncompress(data)

    def append(self, data):
        data = snappy.compress(data)
        return super().append(data)
