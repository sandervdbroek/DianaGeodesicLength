import numpy as np

def readTb(filename,nnodes):
    LArray = np.zeros([nnodes,nnodes])

    # Read file
    with open(filename, 'r') as myFile:
        Read = myFile.readline()
        while Read != '':
            if Read.split() == []:
                Read = myFile.readline()
            elif 'Reference nodenumber' in Read:
                refNode = int(Read.split()[2])
                Read = myFile.readline()
                # Read refNode distances
            elif Read.split()[0].isdigit():
                nodeID = int(Read.split()[0])
                LArray[refNode-1,nodeID-1] = float(Read.split()[1])
                Read = myFile.readline()
            else:
                Read = myFile.readline()
    return LArray

