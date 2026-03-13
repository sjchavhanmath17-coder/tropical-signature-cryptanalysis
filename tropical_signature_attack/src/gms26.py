
import numpy as np
from src.trop_ops import trop_add, trop_mul

m, n, k = 8, 8, 7
MAX_VAL = 255

def keygen():
    X = np.random.randint(0, MAX_VAL+1, size=(m, k))
    Y = np.random.randint(0, MAX_VAL+1, size=(k, n))
    T = trop_mul(X, Y)
    return X, Y, T

def sign(M, X, Y):
    # Sample U such that (M⊗X)⊕U != U
    while True:
        U = np.random.randint(0, MAX_VAL+1, size=(n, k))
        if not np.array_equal(trop_add(trop_mul(M, X), U), U):
            break

    # Sample V such that (Y⊗M)⊕V != V
    while True:
        V = np.random.randint(0, MAX_VAL+1, size=(k, m))
        if not np.array_equal(trop_add(trop_mul(Y, M), V), V):
            break

    A = trop_add(trop_mul(M, X), U)
    B = trop_add(trop_mul(Y, M), V)
    P = trop_mul(X, V)
    R = trop_mul(U, Y)
    S = trop_mul(U, V)
    return {'M': M, 'A': A, 'B': B, 'P': P, 'R': R, 'S': S}

def verify(M, sig, T):
    A, B, P, R, S = sig['A'], sig['B'], sig['P'], sig['R'], sig['S']
    MTM = trop_mul(trop_mul(M, T), M)
    MP = trop_mul(M, P)
    RM = trop_mul(R, M)
    W = trop_add(trop_add(trop_add(MTM, MP), RM), S)
    left = trop_mul(A, B)
    return np.array_equal(left, W) and not np.array_equal(left, S)
