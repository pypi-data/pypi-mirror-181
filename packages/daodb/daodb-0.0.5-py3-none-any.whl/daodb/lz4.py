'''
LZ4 compression module.

Copyright 2022 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

import lz4.frame

class Lz4Mixin:
    '''
    LZ4 compression mix-in.
    '''

    def load_record(self, data_file, pos, size):
        data = super().load_record(data_file, pos, size)
        return lz4.frame.decompress(data)

    def append(self, data):
        data = lz4.frame.compress(data)
        return super().append(data)
