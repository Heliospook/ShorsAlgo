from random import randint
from Classical.GCD import egcd

def pickFromZnStar(n : int)->int:
    a = randint(2, n - 1)
    g, _, __ = egcd(a, n)
    while(g != 1):
        a = randint(2, n - 1)
        g, _, __ = egcd(a, n)
    return a

def _millerRabin(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        is_composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                is_composite = False
                break
        if is_composite:
            return False
    return True

def isPrime(n):
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if n in small_primes:
        return True
    for prime in small_primes:
        if n % prime == 0:
            return False
    return _millerRabin(n, k=20)