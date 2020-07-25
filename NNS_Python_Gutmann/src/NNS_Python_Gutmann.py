#
# Author: Gregory Gutmann
# Nearest neighbor search algorithm demo in python
#
# Made to mirror the C/C++ version, so typical python conventions have likely not been followed.
# Comments or suggestions to accelerate this code are welcomed, it seems far slower than it should be.
# Both C/C++ and python versions are single threaded, but the C/C++ version is 100x the speed.
#

import numpy as np
import matplotlib.pyplot as plt
import time

# This projects files
import globals
import sort
import particle as pt


xDimension = globals.X_DIM
yDimension = globals.Y_DIM
cellSize = globals.CELL_SIZE
gridBuffer = globals.GRID_BUFFER
particleCount = globals.PARTICLE_COUNT


sortObject = sort.NNS()
partObject = pt.Particle()

sortObject.init(particleCount, xDimension, yDimension, cellSize, gridBuffer)
partObject.init(particleCount, xDimension, yDimension)

if(globals.PERFORMANCE_TEST == 0):
    # Run the has function
    sortObject.hashArray(partObject.locations)

    print("\nStarting hash and indices:")
    print(sortObject.keyCellID)
    print(sortObject.valueIndex)

    # Get index ordering that would make the cellID array sorted
    sortObject.getSortedIndex()

    print("\nSorted indices:")
    print(sortObject.valueIndex)

    # Reorder location data and hash based on index order from getSortedIndex
    # Other data use in the future should be reordered here too
    sortObject.reorder(partObject.locations, partObject.sortedLoc)

    print("\nSorted hash:")
    print(sortObject.sortedKeyCellID)

    # Find start and end particle index of each cell
    sortObject.findCellStartEnd()

    print("\nCell start and end:")
    idx = np.arange(sortObject.cellCount)
    print(idx)
    print(sortObject.cellStart)
    print(sortObject.cellEnd)

    # Run the count neighbors function
    partObject.countNeighbors(sortObject)

    print("\nNeighbor count:")
    print(partObject.neighborCount)
    #print(partObject.neighborList)

    # Run the count neighbors function n^2
    partObject.countNeighborsN2(cellSize)

    print("\nNeighborN2 count:")
    print(partObject.neighborCountN2)
    #print(partObject.neighborN2List)

if(globals.PERFORMANCE_TEST == 1):
    # The test has been set to 1000 iterations to mirror the C/C++ version but I recommend running fewer iterations.
    testIterations = 1000

    print("\nStarting performance test\n")

    # Begin the NNS algorithm test 
    start = time.perf_counter()
    for i in range(testIterations):
        sortObject.hashArray(partObject.locations)
        sortObject.getSortedIndex();
        sortObject.reorder(partObject.locations, partObject.sortedLoc)
        sortObject.findCellStartEnd();
        partObject.countNeighbors(sortObject);
    end = time.perf_counter()

    nnsTime = (end - start)
    print("NNS time %0.3f seconds\n" % nnsTime)

    # Begin the O(n^2) algorithm test 
    start = time.perf_counter()
    for i in range(testIterations):
        partObject.countNeighborsN2(cellSize)
    end = time.perf_counter()

    ataTime = (end - start)
    print("All-to-all time %0.3f seconds\n" % ataTime)

    print("Performance difference: %.1fx\n" % (ataTime / nnsTime));

print("Finished")