"""
setup.py file for SWIG example

here successive_average is the module name.
to create a new setup.py file replace the word "successive_average" with the new module name
at all places in the file

the "module_name_wrap.c" file is created by SWIG.

for example, module name is template
template_module = Extension('_template',
                            sources=['template_wrap.c', 'template.c'],
                            )

here "template.c" contains the C code for the module 'template'
"""

from distutils.core import setup, Extension

successive_average_module = Extension('_successive_average',
                                      sources=[
                                          'successive_average_wrap.c', 'successive_average.c'],
                                      )

setup(name='successive_average',
      version='0.1',
      author="SWIG Docs",
      description="""Simple swig example from docs""",
      ext_modules=[successive_average_module],
      py_modules=["successive_average"],
      )
