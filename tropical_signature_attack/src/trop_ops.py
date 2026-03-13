
import numpy as np

def trop_add(A, B):
    return np.minimum(A, B)

def trop_mul(A, B):
    m = A.shape[0]
    n = B.shape[1]
    p = A.shape[1]
    res = np.full((m, n), 10**9, dtype=int)
    for i in range(m):
        for j in range(n):
            mn = 10**9
            for t in range(p):
                val = A[i, t] + B[t, j]
                if val < mn:
                    mn = val
            res[i, j] = mn
    return res
