# create a python file which will call the functions from the
#C file.
#when calling the functions from the C file (these are the functions the
#module offers) use module_name.function_name

#for simplicity, use same name for the .c, .i and .h files.
#however use a variation of that name for the python file because
#SWIG create a python file with that name

#for example
#you have temp.c, temp.h, temp.i file
#the python file should not be named temp.py because SWIG will create temp.py
#and will overwrite your file or may give error.
