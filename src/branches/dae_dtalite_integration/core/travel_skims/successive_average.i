/* File: arrayex.i */

%module successive_average

%{
#include "successive_average.h"
%}

%include "cstring.i"
%cstring_bounded_mutable(char *path, 1024);
%newobject set_file;

char* set_file(char *s);
void print_file_path();

void initialize_ts_array(int nodes_temp);
void set_ts_array(char *file_1, char *file_2, char *file_3, int iteration);

void delete_ts_array();

void print_ts_array();

void delete_file(char *s);
void rename_file(char *s1, char *s2);
void write_avg_ts_to_file();

