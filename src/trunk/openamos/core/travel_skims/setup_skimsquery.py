#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension

skimsquery_module = Extension('_skimsquery',
                            sources=['skimsquery_wrap.c', 'skimsquery.c'],
                            )

setup (name = 'skimsquery',
        version = '0.1',
        author = "SWIG Docs",
        description = """Simple swig example from docs""",
        ext_modules = [skimsquery_module],
        py_modules = ["skimsquery"],
        )
