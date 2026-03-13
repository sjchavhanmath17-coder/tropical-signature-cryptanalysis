
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from src.gms26 import keygen, sign, verify
from src.attacks.malleability import malleability_attack

X, Y, T = keygen()
M = np.random.randint(0, 256, size=(8,8))
sig = sign(M, X, Y)
print("Original signature valid?", verify(M, sig, T))
sig2 = malleability_attack(sig)
if sig2 is not None:
    print("Malleated signature valid?", verify(M, sig2, T))
    print("S matrices different?", not np.array_equal(sig['S'], sig2['S']))
else:
    print("Malleability attack failed (no suitable entry).")
