from random import randint
from Classical.GCD import egcd

def pick_from_ZnStar(n : int)->int:
    a = randint(2, n - 1)
    while(egcd(a, n) != 1):
        a = randint(2, n - 1)
    return a
