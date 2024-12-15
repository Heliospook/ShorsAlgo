from array import array
import math
import fractions
from Classical.GCD import modpow

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
            powTerm = pow(a, den/2)
    
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
