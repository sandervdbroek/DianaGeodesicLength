# Flat plate Diana and analytical comparison
# (c) 2019-06-12 Sander van den Broek
# Leibniz University Hannover


import numpy as np
# from plotFunction import *
from generateOutput import *
from scipy import optimize
from readOutput import *
from runAnalysis import *
# Configuration

lengthX = 1
lengthY = 1.75
elementSizes = [0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5]
# timeSteps = [0.001]
# elementSizes = [0.1]
# elementSizes = [0.2]
i = 3
j = 0
errorArray = np.zeros([3,len(elementSizes)])
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
    DATfilename = "FP175_dX" + str(deltaX) + "_dY" + str(deltaY) + '.dat'
    tbfilename  = "FP175_dX" + str(deltaX) + "_dY" + str(deltaY) + '.tb'
    generateDat(X, F,DATfilename)

    # Create output files and run them
    #error = runAnalysis(DATfilename,timeStep,numberNodes,LengthAnal)
    optiFunc = lambda timeStep: runDiana(DATfilename,timeStep,numberNodes,LengthAnal)
    initialguess = ((deltaX+deltaY)/2)**2
    if initialguess < 0.01:
        initialguess = 0.01
    # optiTime = optimize.minimize(optiFunc,[initialguess], bounds=[(0, None)], method='TNC', options={'disp': True})
    # optiTime = optimize.minimize(optiFunc, [initialguess],  method='Powell', options={'disp': True})
    upperbound = initialguess*100
    optiTime = optimize.minimize_scalar(optiFunc, bounds=(0,upperbound), options={'disp': True})
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
    errorArray[1,elementindex] = optiTime.x
    errorArray[2,elementindex] = RMSerror
    np.savetxt('FPOptivals2m5.csv', errorArray)
    elementindex += 1
# np.save('FPError',errorArray)π