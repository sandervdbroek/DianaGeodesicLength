# Flat plate Diana and analytical comparison
# (c) 2019-06-12 Sander van den Broek
# Leibniz University Hannover


import numpy as np
# from plotFunction import *
from generateOutput import *
import platform
import sys
import os
# Configuration

lengthX = 1
lengthY = 1
# elementSizes = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5]
timeSteps = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
elementSizes = [0.2]
i = 3
j = 0
for elementSize in elementSizes:
    nelemX = round(lengthX/elementSize)
    nelemY = round(lengthY/elementSize)
    numberNodes = (nelemX+1)*(nelemY+1)
    numberElements = nelemX*nelemY
    deltaX = lengthX/nelemX
    deltaY = lengthY/nelemY

    X = np.zeros([numberNodes,3])
    F = np.zeros([numberElements,4],dtype=np.dtype('u4'))

    # Meshing X to Y

    # Nodes
    for k in range(nelemY+1):
        for l in range(nelemX + 1):
            X[l+k*(nelemX+1),:] = [l*deltaX,k*deltaY,0]

    # Connectivity
    for k in range(nelemY):
        for l in range(nelemX):
            F[l + k * nelemX, :] = [l+k*(nelemX+1), l+1+k*(nelemX+1), l+1+(k+1)*(nelemX+1), l+(k+1)*(nelemX+1)]





    #showMeshPlot(X, F)

    #Create length array
    LengthAnal = np.zeros([numberNodes,numberNodes])
    #
    for i in range(numberNodes):
        for j in range(numberNodes):
            1+1
            LengthAnal[i,j] = np.linalg.norm(X[i,:]-X[j,:])
    print('Run completed')
    DATfilename = "FP_dX" + str(deltaX) + "_dY" + str(deltaY) + '.dat'
    generateDat(X, F,DATfilename)

    # Create output files and run them
    for timeStep in timeSteps:
        DCFfilename = "FP_dX" + str(deltaX) + "_dY" + str(deltaY) + "_t" + str(timeStep) + '.dcf'
        OUTfilename = "FP_dX" + str(deltaX) + "_dY" + str(deltaY) + "_t" + str(timeStep)
        generateDcf(DCFfilename,timeStep,numberNodes)
        if 'linux' in sys.platform:
            print('TBD')
        elif 'win32' in sys.platform:
            print('Runnning' + DCFfilename)
            os.system('diana ' + OUTfilename + " " + DATfilename + " " + DCFfilename)
        elif 'darwin' in sys.platform:
            print('Runnning ' + DCFfilename)
            print('TBD OSX')
        else:
            raise RuntimeError("Unsupported operating system: {}".format(sys.platform))


