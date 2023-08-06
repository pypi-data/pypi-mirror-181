# coding=utf-8

import codecs
import re

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
from setup_libuv import libuv_build_ext


def get_version():
    return re.search(r"""__version__\s+=\s+(?P<quote>['"])(?P<version>.+?)(?P=quote)""", open('pyuv/_version.py').read()).group('version')


setup(name             = 'pyuv-kathara',
      version          = get_version(),
      author           = 'Kathara Framework',
      author_email     = 'contact@kathara.org',
      url              = 'http://github.com/saghul/pyuv',
      description      = 'Updated version of pyuv for kathara',
      long_description = codecs.open('README.rst', encoding='utf-8').read(),
      platforms        = ['POSIX', 'Microsoft Windows'],
      classifiers      = [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],
      cmdclass     = {'build_ext': libuv_build_ext},
      packages     = ['pyuv'],
      ext_modules  = [Extension('pyuv._cpyuv',
                                sources = ['src/pyuv.c'],
                     )]
     )

