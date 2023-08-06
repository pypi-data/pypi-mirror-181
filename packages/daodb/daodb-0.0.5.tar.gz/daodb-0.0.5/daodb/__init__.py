'''
DAO DB: Declassed Append-Only Database

Copyright 2022 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

__version__ = '0.0.5'

from .core import DaoDB
from .jsondb import JsonDaoDB, JsonMixin
from .gzip import GzipMixin
from .lzma import LzmaMixin
