#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension

successive_average_module = Extension('_successive_average', 
                            sources=['successive_average_wrap.c', 'successive_average.c'],
                            )
                            
setup (name = 'successive_average',
        version = '0.1',
        author = "SWIG Docs",
        description = """Simple swig example from docs""",
        ext_modules = [successive_average_module],
        py_modules = ["successive_average"],
        )
