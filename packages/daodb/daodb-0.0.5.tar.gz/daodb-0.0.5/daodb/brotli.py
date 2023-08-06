'''
Brotli compression module.

Copyright 2022 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

import brotli

class BrotliMixin:
    '''
    Brotli compression mix-in.
    '''

    def load_record(self, data_file, pos, size):
        data = super().load_record(data_file, pos, size)
        return brotli.decompress(data)

    def append(self, data):
        data = brotli.compress(data)
        return super().append(data)
