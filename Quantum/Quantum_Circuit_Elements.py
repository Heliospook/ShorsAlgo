import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
import math
from Classical.GCD import modinv

# Several components here are heavily inspired from Qiskit components available online
def QFT(ckt, register_u, n, swapsReqd):
    i=n-1
    while i>=0:
        ckt.h(register_u[i])        
        j=i-1  
        while j>=0:
            if (np.pi)/(pow(2,(i-j))) > 0:
                ckt.cp((np.pi) / (pow(2, (i - j))), register_u[j], register_u[i])
                j=j-1   
        i=i-1  
    if swapsReqd==1:
        i=0
        while i < ((n-1)/2):
            ckt.swap(register_u[i], register_u[n-1-i])
            i=i+1

def QFTinv(ckt, register_u, n, swapsReqd):
    if swapsReqd==1:
        i=0
        while i < ((n-1)/2):
            ckt.swap(register_u[i], register_u[n-1-i])
            i=i+1
    i=0
    while i<n:
        ckt.h(register_u[i])
        if i != n-1:
            j=i+1
            y=i
            while y>=0:
                 if (np.pi)/(pow(2,(j-y))) > 0:
                    ckt.cp( - (np.pi)/(pow(2,(j-y))) , register_u[j] , register_u[y] )
                    y=y-1   
        i=i+1

def getAngles(a, N):
    s=bin(int(a))[2:].zfill(N) 
    angles=np.zeros([N])
    for i in range(0, N):
        for j in range(i,N):
            if s[j]=='1':
                angles[N-i-1] += math.pow(2, -(j-i))
        angles[N-i-1]*=np.pi
    return angles

def phaseCC(ckt,angle,ctl1,ctl2,tgt):
    ckt.cp(angle/2,ctl1,tgt)
    ckt.cx(ctl2,ctl1)
    ckt.cp(-angle/2,ctl1,tgt)
    ckt.cx(ctl2,ctl1)
    ckt.cp(angle/2,ctl2,tgt)

def addPhi(ckt,q,a,N,inv):
    angle=getAngles(a,N)
    for i in range(0,N):
        if inv==0:
            ckt.p(angle[i],q[i])
        else:
            ckt.p(-angle[i],q[i])
            
def caddPhi(ckt,q,ctl,a,n,inv):
    angle=getAngles(a,n)
    for i in range(0,n):
        if inv==0:
            ckt.cp(angle[i],ctl,q[i])
        else:
            ckt.cp(-angle[i],ctl,q[i])
    
def ccaddPhi(ckt,q,ctl1,ctl2,a,n,inv):
    angle=getAngles(a,n)
    for i in range(0,n):
        if inv==0:
            phaseCC(ckt,angle[i],ctl1,ctl2,q[i])
        else:
            phaseCC(ckt,-angle[i],ctl1,ctl2,q[i])
        
def ccaddPhimodN(ckt, q, ctl1, ctl2, aux, a, N, n):
    ccaddPhi(ckt, q, ctl1, ctl2, a, n, 0)
    addPhi(ckt, q, N, n, 1)
    QFTinv(ckt, q, n, 0)
    ckt.cx(q[n-1],aux)
    QFT(ckt,q,n,0)
    caddPhi(ckt, q, aux, N, n, 0)
    
    ccaddPhi(ckt, q, ctl1, ctl2, a, n, 1)
    QFTinv(ckt, q, n, 0)
    ckt.x(q[n-1])
    ckt.cx(q[n-1], aux)
    ckt.x(q[n-1])
    QFT(ckt,q,n,0)
    ccaddPhi(ckt, q, ctl1, ctl2, a, n, 0)
    
def ccaddPhimodN_inv(ckt, q, ctl1, ctl2, aux, a, N, n):
    ccaddPhi(ckt, q, ctl1, ctl2, a, n, 1)
    QFTinv(ckt, q, n, 0)
    ckt.x(q[n-1])
    ckt.cx(q[n-1],aux)
    ckt.x(q[n-1])
    QFT(ckt, q, n, 0)
    ccaddPhi(ckt, q, ctl1, ctl2, a, n, 0)
    caddPhi(ckt, q, aux, N, n, 1)
    QFTinv(ckt, q, n, 0)
    ckt.cx(q[n-1], aux)
    QFT(ckt, q, n, 0)
    addPhi(ckt, q, N, n, 0)
    ccaddPhi(ckt, q, ctl1, ctl2, a, n, 1)

def cMULTmodN(ckt, ctl, q, aux, a, N, n):
    QFT(ckt,aux,n+1,0)
    for i in range(0, n):
        ccaddPhimodN(ckt, aux, q[i], ctl, aux[n+1], (2**i)*a % N, N, n+1)
    QFTinv(ckt, aux, n+1, 0)

    for i in range(0, n):
        ckt.cswap(ctl,q[i],aux[i])

    a_inv = modinv(a, N)
    QFT(ckt, aux, n+1, 0)
    i = n-1
    while i >= 0:
        ccaddPhimodN_inv(ckt, aux, q[i], ctl, aux[n+1], math.pow(2,i)*a_inv % N, N, n+1)
        i -= 1
    QFTinv(ckt, aux, n+1, 0)