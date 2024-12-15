from Classical.Power import checkPrimePower
from Randomized.Primes import isPrime
from Quantum.FactorFinder import findFactors

def factorize(n, factors):
    if isPrime(n):
        if factors.get(n, -1) == -1:
            factors[n] = 0
        factors[n] += 1
        return 
    
    an, bn = checkPrimePower(n)
    if an != -1 : 
        if factors.get(an, -1) == -1:
            factors[an] = 0
        factors[an] += bn
    else : 
        d1, d2 = findFactors(n)
        factorize(d1, factors)
        factorize(d2, factors)
        if d1 == -1:
            raise Exception("No factors found")


n = int(input("Enter n, the number to be factored (>=2) : "))
if n <= 1:
    raise ValueError("Use n >= 2")

factors = {}
while n % 2 == 0:
    if factors.get(2, -1) == -1:
        factors[2] = 0
    factors[2] += 1
    n //= 2
    
try : 
    factorize(n, factors)
    for (factor, count) in factors.items():
        print(f"Factor : {factor}, count : {count}")
except Exception as e: 
    print(e)
            
