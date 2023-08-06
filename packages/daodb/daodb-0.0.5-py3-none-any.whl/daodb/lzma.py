'''
LZMA compression module.

Copyright 2022 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

import lzma

class LzmaMixin:
    '''
    LZMA compression mix-in.
    '''

    def load_record(self, data_file, pos, size):
        data = super().load_record(data_file, pos, size)
        return lzma.decompress(data)

    def append(self, data):
        data = lzma.compress(data)
        return super().append(data)
