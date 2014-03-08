%module skimsquery -- python module name

%{
#include "skimsquery.h" -- include the .h file which is included in the .c
%}

%include "carrays.i" -- when using the carrays module
%array_functions(float, floatArray); 
%array_functions(int, intArray);
%include "cstring.i" -- when using the cstring module
%cstring_bounded_mutable(char *path, 1024); 
%newobject set_file;

-- http://www.swig.org/Doc1.3/Library.html
the above link is the tutorial for carrays and cstring with sample code.

-- list all the methods in the .C file

void sample_function();