1) default value of offset is 1
2) file_name_1[] = "temp_data_copy.csv"; --> This file is of the format (nodes, edges). The code reads this file and assigns the valus of nodes and edges.
3) file_name_2[] = "skim1.dat"; --> This file is the skim.dat file which is used to create the entore 2D array.


Below are the commands to compile and run the code:
swig -python arrayexample.i
python setup.py build_ext --inplace
python extensions.py

Uploading only the source code and data files.


Important for windows:
http://www.drlock.com/projects/pyrwi/docs/install.php

C:\Documents and Settings\dhyou\workspace\src\openamos\core\travel_skims>python setup.py build_ext --inplace -cmingw32

install Cygwin.
install MinGW.
download and unzip SWIGwin and move to tghe folder that has MinGw installed.
install PCRE.
change the environment vairable PATH and append the path of the swig folder and the python folder
