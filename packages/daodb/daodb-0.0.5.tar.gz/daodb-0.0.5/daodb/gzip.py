'''
GZip compression module.

Copyright 2022 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

import gzip

from .core import DaoDB


class GzipMixin(DaoDB):
    '''
    GZip compression mix-in.
    '''

    def load_record(self, data_file, pos, size):
        data = super().load_record(data_file, pos, size)
        return gzip.decompress(data)

    def append(self, data):
        data = gzip.compress(data)
        return super().append(data)
