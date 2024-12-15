import math 

class PrimePowerException(Exception):
    def __init__(self, a, b, n):
        self.a, self.b, self.n = a, b, n
        self.message = f"{n} is of the form {a} ^ {b}"
        super().__init__(self.message)  

def checkPrimePower(n : int)->bool:
    """
        There are very few values of b for which a^b can be a prime power. We will run an exhaustive check for all values of b.
    """
    n = int(n)
    blim = math.ceil(math.log2(n))
    for b in range(2, blim):
        # binary search
        l, r = 2, n - 1
        a = l
        while l < r : 
            mid = (l + r)//2
            if (mid ** b) <= n : 
                a = max(a, mid)
                l = mid + 1
            else :
                r = mid - 1
        
        if a ** b == n:
            raise PrimePowerException(a, b, n)
        
    return False

     
def modpow(a, b, M):
    res = 1
    while b > 0:
        if b & 1 : 
           res = (res * a) % M
           a = (a * a) % M 
        b /= 2
    return res