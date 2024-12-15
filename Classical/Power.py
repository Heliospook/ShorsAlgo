import math 

def checkPrimePower(n : int):
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
            return a, b
    return -1, -1

     
def modpow(a, b, M):
    res = 1
    while b > 0:
        if b & 1 : 
           res = (res * a) % M
           a = (a * a) % M 
        b /= 2
    return res