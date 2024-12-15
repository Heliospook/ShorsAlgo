## Shor's Factoring
Subhajeet Lahiri, IMT2021022

---

The given implementation closely follows the one given in class - complete with primality testing, checking prime powers and quantum order finding. The last one has been heavily inspired by Qiskit implementations available online. 

The circuit only works for small values of n (atleast 21). Upwards of that, it becomes extremely slow and doesn't finish running. 

Even for small values like 15 and 21, it may sometimes fail. In that case, the code just needs to be run again.

- The libraries reqd. to run the project are listed in `requirements.txt`