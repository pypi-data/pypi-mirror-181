import os
import setuptools

import daodb

with open(os.path.join(os.path.dirname(__file__), 'README')) as f:
    _long_description = f.read()

setuptools.setup(
    name         = 'daodb',
    version      = daodb.__version__,
    author       = 'AXY',
    author_email = 'axy@declassed.art',
    description  = 'Declassed Append-Only Database',

    long_description = _long_description,
    long_description_content_type = 'text/x-rst',

    url = 'https://declassed.art/repository/daodb',

    packages = [
        'daodb'
    ],

    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Intended Audience :: Developers',
        'Development Status :: 1 - Planning',
        'Topic :: Database :: Database Engines/Servers'
    ],

    python_requires = '>=3.6',
)
