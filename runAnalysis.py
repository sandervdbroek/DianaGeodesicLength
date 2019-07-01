import os
import sys
import subprocess
from readOutput import *
from generateOutput import *
def runDiana(DATfilename,timeStep,numberNodes,LengthAnal):
    DCFfilename = os.path.splitext(DATfilename)[0] + '.dcf'
    FFfilename = os.path.splitext(DATfilename)[0] + '.ff'
    OUTfilename = os.path.splitext(DATfilename)[0]
    generateDcf(DCFfilename, timeStep, numberNodes)
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
        LArrayDiana = readTb(tbFile, numberNodes)
        LError = LengthAnal - LArrayDiana
        LRelError = LError / (LengthAnal + np.identity(numberNodes))

        # Calculate RMS error
        RMSerror = 0
        for i in range(numberNodes):
            for j in range(numberNodes):
                RMSerror = LRelError[i, j] ** 2 + RMSerror
        RMSerror = np.sqrt(RMSerror / (numberNodes * numberNodes))
        print('t=' + str(timeStep) + ' ' + str(RMSerror))
    else:
        print('WARNING: Failed run detected, skipping output!')
        RMSerror = np.inf
    return RMSerror