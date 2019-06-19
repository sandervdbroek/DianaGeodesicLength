import numpy as np
import datetime

def generateDat(X,F,filename):
    now = datetime.datetime.now()

    f = open(filename, "w+")
    f.write(f": Diana DATfile written by Sander's automated Python script {now.isoformat()}\n\
'DIRECTIONS' \n\
   1   1.00000E+00   0.00000E+00   0.00000E+00 \n\
   2   0.00000E+00   1.00000E+00   0.00000E+00 \n\
   3   0.00000E+00   0.00000E+00   1.00000E+00 \n\
'MODEL' \n\
DIMENS \"2D\" \n\
GRAVDI 2\n\
GRAVAC  -9.81000E+00\n\
'COORDINATES'\n\
")
    for node in range(len(X[:,0])):
        f.write(f"{node+1:5d} {X[node,0]} {X[node,1]} {X[node,2]} \n")
    f.write(f"'MATERI' \n\
   1 YOUNG    2.10000E+11\n\
     POISON   3.00000E-01\n\
     DENSIT   7.80000E+03\n\
     CAPACI   1.00000E+00\n\
     CONDUC   1.00000E+00\n\
'GEOMET'\n\
   1 THICK    1.00000E-01\n\
'ELEMENTS'\n\
SET  \"Sheet 1\"\n\
CONNECT\n")
    for el in range(len(F[:,0])):
        f.write(f"{el+1:5d} Q8MEM  {F[el,0]+1} {F[el,1]+1} {F[el,2]+1} {F[el,3]+1} \n")
    f.write(f"MATERIAL 1\n\
GEOMETRY 1\n\
'LOADS'\n\
CASE 1\n\
NAME 'DUMMY'\n\
'END'")

def generateDcf(filename,timestep,nnodes):
    f = open(filename, "w+")
    f.write(f"*FILOS\n\
INITIA\n\
*INPUT\n\
*RANFLD\n\
  BEGIN GEODET\n\
    DTIME {timestep}\n\
    REFNOD 1-{nnodes}\n\
    BEGIN OUTPUT TABULA\n\
      LAYOUT LINPAG 1000000\n\
      BEGIN SELECT \n\
        NODES 1-{nnodes} /\n\
      END SELECT\n\
      DISTAN\n\
    END OUTPUT\n\
    BEGIN OUTPUT NDIANA\n\
      DISTAN\n\
    END OUTPUT\n\
  END GEODET\n\
*END")