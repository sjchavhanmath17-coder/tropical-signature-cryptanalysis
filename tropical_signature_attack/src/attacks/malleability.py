
import numpy as np
from src.trop_ops import trop_mul

def malleability_attack(sig):
    A, B, S = sig['A'], sig['B'], sig['S']
    W = trop_mul(A, B)
    # Find an entry where S[i,j] > W[i,j]
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            if S[i, j] > W[i, j]:
                S_new = S.copy()
                delta = np.random.randint(1, 256)
                S_new[i, j] = S[i, j] + delta
                new_sig = sig.copy()
                new_sig['S'] = S_new
                return new_sig
    # No suitable entry found (extremely unlikely for random signatures)
    return None
