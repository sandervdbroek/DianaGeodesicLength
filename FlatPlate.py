# Flat plate Diana and analytical comparison
# (c) 2019-06-12 Sander van den Broek
# Leibniz University Hannover


import numpy as np
# from plotFunction import *
from generateOutput import *
import platform
import sys
import os
import subprocess
from readOutput import *
# Configuration

lengthX = 1
lengthY = 1
elementSizes = [0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.5]
timeSteps = [0.0001, 0.0005, 0.001, 0.0025, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.125, 0.15, 0.2, 0.3, 0.4, 0.5]
# timeSteps = [0.001]
# elementSizes = [0.2]
i = 3
j = 0
errorArray = np.zeros([len(elementSizes),len(timeSteps)])
elementindex = 0
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
    tindex = 0
    for timeStep in timeSteps:
        DCFfilename = "FP_dX" + str(deltaX) + "_dY" + str(deltaY) + "_t" + str(timeStep) + '.dcf'
        OUTfilename = "FP_dX" + str(deltaX) + "_dY" + str(deltaY) + "_t" + str(timeStep)
        FFfilename =  "FP.ff"
        generateDcf(DCFfilename,timeStep,numberNodes)
        if 'linux' in sys.platform:
            print('TBD')
        elif 'win32' in sys.platform:
            print('Runnning ' + DCFfilename)
            outStatus = subprocess.call('diana ' + OUTfilename + " " + DATfilename + " " + DCFfilename + ' ' + FFfilename)
            print('Outstatus is ' + str(outStatus))
        elif 'darwin' in sys.platform:
            print('Runnning ' + DCFfilename)
            print('TBD OSX')
        else:
            raise RuntimeError("Unsupported operating system: {}".format(sys.platform))
        tbFile = OUTfilename + '.tb'
        if os.path.isfile(tbFile):
            LArrayDiana = readTb(tbFile,numberNodes)
            LError = LengthAnal-LArrayDiana
            LRelError = LError / (LengthAnal + np.identity(numberNodes))

            # Calculate RMS error
            RMSerror = 0
            for i in range(numberNodes):
                for j in range(numberNodes):
                   RMSerror  = LRelError[i,j]**2 + RMSerror
            RMSerror = np.sqrt(RMSerror/(numberNodes*numberNodes))
            errorArray[elementindex,tindex] = RMSerror
            print('t=' + str(timeStep) + ' ' + str(RMSerror))
        else:
            print('WARNING: Failed run detected, skipping output!')
        tindex += 1
    np.save('FPError', errorArray)
    np.savetxt('FPError.csv', errorArray)
    elementindex += 1
# np.save('FPError',errorArray)