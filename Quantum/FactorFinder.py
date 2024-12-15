from Randomized.Primes import pickFromZnStar
from Quantum.Quantum_Circuit_Elements import *

from array import array
import math
import fractions

import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator

class IllegalContinuedFractionException(Exception):
    def __init__(self, message):
        message = "Illegal Continued Fraction  : " + message
        super().__init__(message)

def getFactorsFromPhase(x, tlim, n, a):
    if x <=0:
        raise IllegalContinuedFractionException(f"{x} <= 0")
    T = pow(2, tlim) 
    b, t = array('i'), array('f')
    b.append(math.floor(x/T))
    t.append(x/T - b[0])
    
    i=0
    while i>=0:
        if i>0:
            b.append(math.floor(1 / t[i-1])) 
            t.append((1 / t[i-1]) - b[i])
        xa = 0
        j=i
        while j>0:    
            xa = 1 / ( b[j] + xa )      
            j = j-1
        xa = xa + b[0]
        frac = fractions.Fraction(xa).limit_denominator()
        den=frac.denominator
        i=i+1
        if (den%2) == 1:
            if i>=15:
                raise IllegalContinuedFractionException("Too many tries")
            continue
        powTerm = 0
        
        if den < 1000:
            powTerm = pow(a, (den/2))

        if math.isinf(powTerm)==1 or powTerm>2000000000:
            raise IllegalContinuedFractionException("Denominator too big")

        xplus1 = int(powTerm + 1)
        xminus1 = int(powTerm - 1)
        d1, d2 = math.gcd(xplus1,n), math.gcd(xminus1, n)

        if d1==1 or d1==n or d2==1 or d2==n:
            if t[i-1]==0:
                raise IllegalContinuedFractionException("Couldn't compute solution")
            if i>=15:
                raise IllegalContinuedFractionException("Too many tries") 
        else:
            return d1, d2

def findFactors(N):
    a = pickFromZnStar(N)
    n = math.ceil(math.log(N,2))
    
    aux = QuantumRegister(n+2)
    register_u = QuantumRegister(2*n)
    register_d = QuantumRegister(n)
    classical_u = ClassicalRegister(2*n)
    circuit = QuantumCircuit(register_d , register_u , aux, classical_u)
    circuit.h(register_u)
    circuit.x(register_d[0])
    
    for i in range(0, 2*n):
        cMULTmodN(circuit, register_u[i], register_d, aux, int(pow(a, pow(2, i))), N, n)
    QFTinv(circuit, register_u, 2*n ,1)
    circuit.measure(register_u, classical_u)

    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)
    simulation = simulator.run(compiled_circuit, shots=1024)

    sim_result = simulation.result()
    counts_result = sim_result.get_counts(circuit)
    i=0
    while i < len(counts_result):
        output_desired = list(sim_result.get_counts().keys())[i]
        x_value = int(output_desired, 2)
        try :    
            d1, d2 = getFactorsFromPhase(int(x_value),int(2*n),int(N),int(a))
            return d1, d2
        except IllegalContinuedFractionException as e:
            i += 1
    raise Exception("Factors not found")