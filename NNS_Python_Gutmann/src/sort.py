#
# Author: Gregory Gutmann
# Nearest neighbor search algorithm demo in python
#

import numpy as np

import globals

class NNS(object):
    """description of class"""

    cellLength : int
    bufferSize : int # as a buffer and to handle truncation from dividing by cell size problem

    cellCount : int
    nonBufferCellEstimate : int

    cellDimx : int
    cellDimy : int

    simDimx_buffered : float
    simDimy_buffered : float

    cellStart = np.empty(1, dtype=int, order='C')
    cellEnd = np.empty(1, dtype=int, order='C')

    particleCount : int

    keyCellID = np.empty(1, dtype=int, order='C')       # To be filled in by hash function
    sortedKeyCellID = np.empty(1, dtype=int, order='C') # A buffer to reorder
    valueIndex = np.empty(1, dtype=int, order='C')      # Output of argsort, and used to put data in sorted order based on cellID (hash)

    def init(self, count : int, dimx : int, dimy : int, cell : int, buffer : int):
        self.particleCount = count

        # Multiply buffer by two to get that amount of buffer on all sides
        self.simDimx_buffered = dimx + buffer * 2.0
        self.simDimy_buffered = dimy + buffer * 2.0

        # Truncation will likely occur here, be careful
        self.cellDimx = int(self.simDimx_buffered / cell)
        self.cellDimy = int(self.simDimy_buffered / cell)

        self.cellLength = cell
        self.bufferSize = buffer
        self.cellCount = self.cellDimx * self.cellDimy

        self.nonBufferCellEstimate = (dimx / cell) * (dimy / cell) # Not used in algorithm

        self.cellStart = np.resize(self.cellStart, self.cellCount)
        self.cellEnd = np.resize(self.cellEnd, self.cellCount)

        self.keyCellID = np.resize(self.keyCellID, count)
        self.sortedKeyCellID = np.resize(self.sortedKeyCellID, count)
        self.valueIndex = np.resize(self.valueIndex, count)

        print("Sort object has been initialized")

    def hashArray(self, locations : np.float):
        xShift = self.simDimx_buffered / 2.0
        yShift = self.simDimy_buffered / 2.0

        for i in range(self.particleCount):
            xCube = int((locations[i * globals.DC + 0] + xShift) / self.cellLength)
            yCube = int((locations[i * globals.DC + 1] + yShift) / self.cellLength)

            hash = xCube + yCube * self.cellDimx

            if (hash >= self.cellCount or hash < 0):
                if(globals.DEBUG == 1):
                    print("Hash ERROR: HashVal %u - Max HashVal %u, c(%u,%u) l(%f,%f)\n" % (hash, self.cellCount, xCube, yCube, locations[i * 2 + 0], locations[i * 2 + 1]));
    
                hash = self.cellCount - 1 # In calculation this cell is excluded (it is in the outter buffer region)
        

            self.keyCellID[i] = hash
            self.valueIndex[i] = i

    def hash(self, x : float, y : float):
        xShift : float = self.simDimx_buffered / 2.0
        yShift : float = self.simDimy_buffered / 2.0

        xCube : int = int(x + xShift) / self.cellLength
        yCube : int = int(y + yShift) / self.cellLength

        hash : int = xCube + yCube * self.cellDimx

        if (hash >= cellCount or hash < 0):
            if(globals.DEBUG == 1):
                print("Hash ERROR: HashVal %u - Max HashVal %u, c(%u,%u) l(%f,%f)\n" % (hash, self.cellCount, xCube, yCube, locations[i * 2 + 0], locations[i * 2 + 1]));
    
            hash = self.cellCount - 1 # In calculation this cell is excluded (it is in the outer buffer region)
        

        return hash

    def getSortedIndex(self):
        self.valueIndex = np.argsort(self.keyCellID) 

    def reorder(self, locations : np.float, sortedLoc : np.float):
        for i in range(self.particleCount):
            originalIndex : int = self.valueIndex[i];

            sortedLoc[i * globals.DC + 0] = locations[originalIndex * globals.DC + 0];
            sortedLoc[i * globals.DC + 1] = locations[originalIndex * globals.DC + 1];
            self.sortedKeyCellID[i] = self.keyCellID[originalIndex];

    def findCellStartEnd(self):

        # Memset to signal cells are empty if not set in this function
        self.cellStart = np.full(self.cellCount, -1, dtype = int)

        # The following line isn't needed, but is run to make printing out the cellEnd array easier to read 
        self.cellEnd = np.full(self.cellCount, -1, dtype = int)

        current : int = -1;

        for i in range(self.particleCount):
            cell = self.sortedKeyCellID[i];
            if (cell != current): # Found entry in new cell
                self.cellEnd[current] = i;
                self.cellStart[cell] = i;
                current = cell;

        self.cellEnd[current] = self.particleCount; # Handle last item

