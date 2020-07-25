#
# Author: Gregory Gutmann
# Nearest neighbor search algorithm demo in python
#

import numpy as np
import random

import globals
import sort

class Particle(object):
	count : int = 0

	locations = np.empty(1, dtype=float, order='C')
	sortedLoc = np.empty(1, dtype=float, order='C')
	neighborCount = np.empty(1, dtype=int, order='C')

	# Testing (N2 stands for n squared, O(n^2) efficiency)
	neighborCountN2 = np.empty(1, dtype=int, order='C')

	# Checking found particles, 2D list
	neighborList = [[]]
	neighborN2List = [[]]

	def init(self, particleCount : int, dimx : int, dimy : int):
		halfDimx : float = dimx / 2.0
		halfDimy : float = dimy / 2.0

		self.count = particleCount

		# Resize arrays
		self.locations = np.empty(particleCount * globals.DC, dtype=float, order='C')
		
		# Resize location arrays based on particle count and Dimension Count
		self.locations = np.resize(self.locations, particleCount * globals.DC)
		self.sortedLoc = np.resize(self.sortedLoc, particleCount * globals.DC)

		# Set neighbor counts to zero
		self.neighborCount = np.zeros(particleCount, dtype=int, order='C')
		self.neighborCountN2 = np.zeros(particleCount, dtype=int, order='C')

		# Place particles at random locations
		for i in range(particleCount):
			xLoc : float = random.uniform(-halfDimx + 0.1, halfDimx - 0.1) # Real-valued distribution
			yLoc : float = random.uniform(-halfDimy + 0.1, halfDimy - 0.1) # Return a random floating point number N such that a <= N <= b
			self.locations[i * globals.DC + 0] = xLoc
			self.locations[i * globals.DC + 1] = yLoc

		# Create empty 2D lists
		self.neighborList = [[] for i in range(particleCount)]
		self.neighborN2List = [[] for i in range(particleCount)]

		print("Particle object has been initialized")

	# All-to-all interaction algorithm O(n^2)
	def countNeighborsN2(self, cellLength : int):
	
		for currIdx  in range(self.count):
			thisLoc_x = float(self.locations[currIdx * globals.DC + 0])
			thisLoc_y = float(self.locations[currIdx * globals.DC + 1])

			localCount : int = 0

			for checkIdx in range(self.count):
				if (checkIdx != currIdx ): # Don't compute with its self
			
					checkIdxLoc_x = float(self.locations[checkIdx * globals.DC + 0])
					checkIdxLoc_y = float(self.locations[checkIdx * globals.DC + 1])
					
					# Careful with vectors direction for your application
					p2pVec_x = float(checkIdxLoc_x - thisLoc_x)
					p2pVec_y = float(checkIdxLoc_y - thisLoc_y)

					dist = np.sqrt((p2pVec_x * p2pVec_x) + (p2pVec_y * p2pVec_y))
					if (dist < float(cellLength)):
						localCount = localCount + 1

						if(globals.PERFORMANCE_TEST == 0):
							self.neighborN2List[currIdx].append(checkIdx)

			self.neighborCountN2[currIdx] = localCount

	# Using the NNS to run "short" range algorithm
	def countNeighbors(self, sort : sort.NNS):
	
		for currIdx  in range(self.count):
			thisLoc_x = float(self.sortedLoc[currIdx * globals.DC + 0])
			thisLoc_y = float(self.sortedLoc[currIdx * globals.DC + 1])
			thisCell = sort.sortedKeyCellID[currIdx]
			originalIndex = sort.valueIndex[currIdx]

			localCount : int = 0;

			# Check the cells around the particle 
			for t  in range(9):
				# Iterate through the nine neighbor cells
				targetCell = int((thisCell - sort.cellDimx + (int((t) / 3) * sort.cellDimx)) - 1 + int((t) % 3));

				if (targetCell < sort.cellCount - 1): # Excludes the one out-of-bounds cell
					startIndex = int(sort.cellStart[targetCell]);
					endIndex = int(sort.cellEnd[targetCell]);

					if (startIndex != -1): # check to see if cell is not empty
						for checkIdx  in range(startIndex, endIndex): # This iterator is going through indexes of the sorted data
							# If data is not sorted will need to use the result of the keyValue sort to get the unsorted (original) index

							if (checkIdx != currIdx): # Don't compute with its self
								checkIdxLoc_x = float(self.sortedLoc[checkIdx * globals.DC + 0])
								checkIdxLoc_y = float(self.sortedLoc[checkIdx * globals.DC + 1])
								
								# Careful with vectors direction for your application
								p2pVec_x = float(checkIdxLoc_x - thisLoc_x)
								p2pVec_y = float(checkIdxLoc_y - thisLoc_y)
								dist = np.sqrt((p2pVec_x * p2pVec_x) + (p2pVec_y * p2pVec_y))

								if (dist < float(sort.cellLength)):
									localCount = localCount + 1

									if(globals.PERFORMANCE_TEST == 0):
										# Get checkIdx's unsorted index to access unsorted data
										checkOrig = sort.valueIndex[checkIdx];
										self.neighborList[originalIndex].append(checkOrig);

			self.neighborCount[originalIndex] = localCount