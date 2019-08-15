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
lengthY = 1
lengthZ = 2
elementSizes = [0.125, 0.15, 0.2, 0.25, 0.3, 0.35, 0.5]
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
    nelemZ = round(lengthZ / elementSize)
    numberNodes = (nelemX+1)*(nelemY+1)*(nelemZ+1)
    numberElements = nelemX*nelemY*nelemZ
    deltaX = lengthX/nelemX
    deltaY = lengthY/nelemY
    deltaZ = lengthZ / nelemZ

    X = np.zeros([numberNodes,3])
    F = np.zeros([numberElements,8],dtype=np.dtype('u4'))

    # Meshing X to Y

    # Nodes
    for k in range(nelemZ+1):
        for l in range(nelemY + 1):
            for m in range(nelemX + 1):
                X[m+k*(nelemX+1)*(nelemY+1)+l*(nelemX+1),:] = [m*deltaX,l*deltaY,k*deltaZ]

    # Connectivity
    for k in range(nelemZ):
        for l in range(nelemY):
            for m in range(nelemX):
                nnx = nelemX+1
                nny = nelemY+1
                p1 = m + nnx * l + nnx*nny * k
                p2 = p1 + 1
                p3 = p2 + nnx
                p4 = p1 + nnx
                p5 = p1 + nnx*nny
                p6 = p2 + nnx*nny
                p7 = p3 + nnx*nny
                p8 = p4 + nnx*nny
                F[m + l * nelemX + k * nelemY * nelemX, :] = [p1, p2, p3, p4, p5, p6, p7, p8]
                # F[l + k * nelemX + m * nelemX * nelemZ, :] = [p1, p2, p3, p4, p5, p6, p7, p8]





    #showMeshPlot(X, F)

    #Create length array
    LengthAnal = np.zeros([numberNodes,numberNodes])
    #
    for i in range(numberNodes):
        for j in range(numberNodes):
            1+1
            LengthAnal[i,j] = np.linalg.norm(X[i,:]-X[j,:])
    print('Run completed')
    DATfilename = "CUBE112_dX" + str(deltaX) + "_dY" + str(deltaY) + '.dat'
    tbfilename  = "CUBE112_dX" + str(deltaX) + "_dY" + str(deltaY) + '.tb'
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
    np.savetxt('CubeOptivals112.csv', errorArray)
    elementindex += 1
# np.save('FPError',errorArray)