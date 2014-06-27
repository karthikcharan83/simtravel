#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

import numpy as np

from distutils.core import setup, Extension

skimsquery_new_module = Extension('_skimsquery',
                              sources=['skimsquery.c', 'skimsquery.i'],
                              include_dirs=[np.get_include()]
                              )

setup(name='skimsquery_new',
      version='0.1',
      author="SWIG Docs",
      description="""Simple swig example from docs""",
      ext_modules=[skimsquery_new_module],
      py_modules=["skimsquery_new"],
      )
