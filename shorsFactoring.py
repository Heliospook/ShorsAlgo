from Classical.Power import checkPrimePower
from Quantum.OrderFinder import findOrder

n = int(input("Enter n : "))
a = int(input("Enter a : "))

try : 
    isPrimePower = checkPrimePower(n)
    order = findOrder(a, n)
    print(f"The order of {a} wrt to {n} is {order}")
except Exception as e: 
    print(e.message)
