#!/usr/bin/python

"""
This script calculates the generalized SVD(GSVD) for N>2 matrices. This is referred to as the higher-order
GSVD(HOGSVD). This is based upon work done by Ponnapalli, Alter et al in the paper: 
Ponnapalli, Sri Priya, et al. "A higher-order generalized singular value decomposition for comparison of global mRNA expression 
from multiple organisms." PloS one 6.12 (2011): e28072.

Usage : "hogsvd.py -m textFileWithMatrixD1 -m textFileWithMatrixD2 -m textFileWithMatrixD3 -o outputDir"

Notes:

1.outputDir will contain the text files, with U and Sigma matrices for each of the input matrices specified by the -m switch. 
A single file in the output directory is created for the shared subspace V.
2. When only two matrices are specified, the QR-decomposition based algorithm is called from LAPACK.
3. When three or more matrices are specified the algorithm specified in the paper is called. This algorithm in *not* based on the
   QR decomposition.
   a. The algorithm is as follows(ref. Ponnapalli et al.):
      i. For each input matrix Di form Ai=Di^T*Di
      ii. Using all Ai,Aj pairs calculate the balanced sum Sij
      iii. Sum over all i,j ~ Si,j to get S
      iv. Do eigen-decomposition on S --> get V and L(Lambda).
      v. Solve a linear system of equations for each Di and V to get Bi
      vi. Normalize columns of Bi to get Ui, norm of the columns form the elements of elements of the diagonal matrix Sigma_i
4. sggsvd(jobu,jobv,jobq,m,n,p,k,l,a,b,alpha,beta,u,v,q,work,iwork,info,lda=shape(a,0),ldb=shape(b,0),ldu=shape(u,0),ldv=shape(v,0),ldq=shape(q,0))

"""

import numpy as np
import sys
from cmdline import processCommandLine
import thgsvd as ho
import shgsvd as so
import writeMat as wm
usage = "hogsvd.py -m textFileWithMatrixA -m textFileWithMatrixB -m textFileWithMatrixC  -o outputDir (-l lapack optional for N=2 matrices)"

    
def main(argv):
    
    (matList,outDir,useLapack)=processCommandLine(argv)
    
    nMatrices=len(matList)
    
    if nMatrices==1:
        A=matList[0]
        (U,S,V)=np.linalg.svd(A)
        wm.writeMat(outDir,"U",U)
        wm.writeMat(outDir,"S",S)
        wm.writeMat(outDir,"V",V)
        
    elif nMatrices==2 and useLapack==True:
        A=matList[0]
        B=matList[1]
        (a,b,alpha,beta,u,v,q)=so.gsvd(A,B)

    elif nMatrices>=2 and useLapack==False:
        uMatList,sigList,V=ho.calcHOGSVD(matList)
        
        ct=0
        for U in uMatList:
            ct=ct+1
            wm.writeMat(outDir,"U%d"%ct,U)

        ct=0
        for sig in sigList:
            ct=ct+1
            wm.writeMat(outDir,"S%d"%ct,sig)

        wm.writeMat(outDir,"V",V)
        
if __name__=="__main__":
    main(sys.argv)
