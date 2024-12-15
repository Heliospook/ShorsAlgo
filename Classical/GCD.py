class NotCoprime(Exception):
    def __init__(self, a, M):
        self.a, self.M = a, M
        self.message(f"{a} and {M} are not coprime, Modular inverse of {a} wrt to {M} doesn't exist.")
        super().__init__(self.message)
    
def egcd(a : int, b : int) -> tuple[int, int, int]:
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        x, y = y, x
        return (g, x - (b // a) * y, y)

def modinv(a : int, M : int) -> tuple[int, int, int]:
    g, x, y = egcd(a, M)
    if g != 1:
        raise NotCoprime(a, M)
    return x % M