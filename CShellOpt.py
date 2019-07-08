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
from runAnalysis import *
# Configuration

R = 1
lengthZ = 1
elementSizes = [0.075, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.5]
# timeSteps = [0.0001, 0.0005, 0.001, 0.0025, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.125, 0.15, 0.2, 0.3, 0.4, 0.5]
# timeSteps = [0.04]
# elementSizes = [0.2]

errorArray = np.zeros([len(elementSizes),len(timeSteps)])
elementindex = 0
for elementSize in elementSizes:
    nelemZ = round(lengthZ / elementSize)
    nelelemD = round(2*R*np.pi/elementSize)
    numberNodes = nelelemD*(nelemZ+1)
    numberElements = nelelemD*nelemZ
    deltaPhi = 2*np.pi/nelelemD
    deltaZ = lengthZ / nelemZ

    X = np.zeros([numberNodes,3])
    F = np.zeros([numberElements,4],dtype=np.dtype('u4'))

    # Meshing X to Y

    # Nodes
    for k in range(nelemZ+1):
        for l in range(nelelemD):
            X[l+k * nelelemD,:] = [R*np.sin(deltaPhi*l),-R*np.cos(deltaPhi*l),k*deltaZ]

    # Connectivity
    for k in range(nelemZ):
        for l in range(nelelemD):
            if l+1 == nelelemD:
                F[l + k * nelelemD, :] = [l + nelelemD*k,  nelelemD*k,  nelelemD*(k+1), l + nelelemD*(k+1)]
            else:
                F[l + k * nelelemD, :] = [l +nelelemD*k, l + 1+nelelemD*k, l + 1+nelelemD*(k+1), l +nelelemD*(k+1)]





    #showMeshPlot(X, F)

    #Create length array
    LengthAnal = np.zeros([numberNodes,numberNodes])
    #
    dDel = np.linalg.norm(X[0,:] - X[1,:])
    for i in range(numberNodes):
        for j in range(numberNodes):
            dZ = np.abs(X[i,2] - X[j,2])
            temp1 = np.mod(i, nelelemD)
            temp2 = np.mod(j, nelelemD)
            if temp1 > temp2:
                segs = min([np.abs(temp1-temp2), np.abs(temp1-nelelemD)+temp2])
            elif temp2 > temp1:
                segs = min([np.abs(temp2 - temp1), np.abs(temp2 - nelelemD) + temp1])
            else:
                segs = 0
            LengthAnal[i,j] = np.sqrt(dZ**2+(segs*dDel)**2)
    print('Run completed')
    DATfilename = "CShell_dTh" + str(deltaPhi) + "_dz" + str(deltaZ) + '.dat'
    generateDat(X, F,DATfilename)

    # Create output files and run them
    optiFunc = lambda timeStep: runDiana(DATfilename, timeStep, numberNodes, LengthAnal)
    initialguess = ((deltaX + deltaY) / 2) ** 2
    if initialguess < 0.01:
        initialguess = 0.01
    # optiTime = optimize.minimize(optiFunc,[initialguess], bounds=[(0, None)], method='TNC', options={'disp': True})
    # optiTime = optimize.minimize(optiFunc, [initialguess],  method='Powell', options={'disp': True})
    upperbound = initialguess * 100
    optiTime = optimize.minimize_scalar(optiFunc, bounds=(0, upperbound), options={'disp': True})
    runDiana(DATfilename, optiTime.x, numberNodes, LengthAnal)
    LArrayDiana = readTb(tbfilename, numberNodes)
    LError = LengthAnal - LArrayDiana
    LRelError = LError / (LengthAnal + np.identity(numberNodes))
    # Calculate RMS error
    RMSerror = 0
    for i in range(numberNodes):
        for j in range(numberNodes):
            RMSerror = LRelError[i, j] ** 2 + RMSerror
    RMSerror = np.sqrt(RMSerror / (numberNodes * numberNodes))
    print('t=' + str(optiTime.x) + ' ' + str(RMSerror))
    print('Timestep for elemsize ' + str(elementSize) + ' ' + str(optiTime.x))
    print('Error is ' + str(LRelError))
    # np.save('FPError', errorArray)
    # np.savetxt('FPError.csv', errorArray)
    errorArray[0, elementindex] = deltaX
    errorArray[1, elementindex] = optiTime.x
    errorArray[2, elementindex] = RMSerror
    np.savetxt('CShellOpt.csv', errorArray)
    elementindex += 1
# np.save('FPError',errorArray)