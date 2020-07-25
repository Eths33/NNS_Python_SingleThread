#
# Author: Gregory Gutmann
# Nearest neighbor search algorithm demo in python
#

PERFORMANCE_TEST = 0
DEBUG = 1
DC = 2                  # Count of dimensions 2D here, setting it to 3 will not make it 3D currently

if (PERFORMANCE_TEST == 0):
    X_DIM = int(10)
    Y_DIM = int(10)
    CELL_SIZE = int(5)
    GRID_BUFFER = int(5) # two times the cell size is a good starting point
    PARTICLE_COUNT = int(20)
else:
    X_DIM = int(100)
    Y_DIM = int(100)
    CELL_SIZE = int(5)
    GRID_BUFFER = int(10) # two times the cell size is a good starting point
    PARTICLE_COUNT = int(800)


# Resources

# C/C++ version of the code
# https://github.com/Eths33/NNS_Cpp_SingleThread

# Init empty numpy
# https://www.w3resource.com/numpy/array-creation/empty.php

# Numpy resize
# https://numpy.org/doc/stable/reference/generated/numpy.resize.html

# Including other code files
# https://blog.tecladocode.com/python-30-day-21-multiple-files/

# Python structs 
# https://stackoverflow.com/questions/35988/c-like-structures-in-python

# Python data types
# https://www.w3schools.com/python/python_datatypes.asp

# Python classes 
# https://www.w3schools.com/python/python_classes.asp

# Using things from other files in Python
# https://kite.com/python/answers/how-to-import-variables-from-another-file-in-python

# argsort - Returns the indices that would sort an array.
# https://numpy.org/doc/stable/reference/generated/numpy.argsort.html

# full - set values of an array 
# https://numpy.org/doc/stable/reference/generated/numpy.full.html#numpy.full