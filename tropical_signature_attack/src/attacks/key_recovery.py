
import numpy as np
from z3 import Solver, Int, And, sat
from src.trop_ops import trop_mul
from src.attacks.utils import add_min

def recover_from_signatures(sig_list, T, dims=(8,8,7), max_val=255, timeout=None):
    m, n, k = dims
    s = Solver()
    if timeout is not None:
        s.set("timeout", timeout * 1000)

    X = [[Int(f'X_{i}_{j}') for j in range(k)] for i in range(m)]
    Y = [[Int(f'Y_{i}_{j}') for j in range(n)] for i in range(k)]

    U_vars = []
    V_vars = []
    for idx in range(len(sig_list)):
        U = [[Int(f'U{idx}_{i}_{j}') for j in range(k)] for i in range(n)]
        V = [[Int(f'V{idx}_{i}_{j}') for j in range(m)] for i in range(k)]
        U_vars.append(U)
        V_vars.append(V)

    all_vars = sum(X, []) + sum(Y, [])
    for u_mat in U_vars:
        all_vars += sum(u_mat, [])
    for v_mat in V_vars:
        all_vars += sum(v_mat, [])
    for var in all_vars:
        s.add(And(var >= 0, var <= max_val))

    # Public key constraints
    for i in range(m):
        for j in range(n):
            terms = [X[i][l] + Y[l][j] for l in range(k)]
            add_min(s, T[i, j], terms)

    # Signature constraints
    for idx, sig in enumerate(sig_list):
        M = sig['M']; A = sig['A']; B = sig['B']; P = sig['P']; R = sig['R']; S = sig['S']
        U = U_vars[idx]; V = V_vars[idx]

        for i in range(n):
            for j in range(k):
                terms = [int(M[i, l]) + X[l][j] for l in range(m)] + [U[i][j]]
                add_min(s, A[i, j], terms)

        for i in range(k):
            for j in range(m):
                terms = [Y[i][l] + int(M[l, j]) for l in range(n)] + [V[i][j]]
                add_min(s, B[i, j], terms)

        for i in range(m):
            for j in range(m):
                terms = [X[i][l] + V[l][j] for l in range(k)]
                add_min(s, P[i, j], terms)

        for i in range(n):
            for j in range(n):
                terms = [U[i][l] + Y[l][j] for l in range(k)]
                add_min(s, R[i, j], terms)

        for i in range(n):
            for j in range(m):
                terms = [U[i][l] + V[l][j] for l in range(k)]
                add_min(s, S[i, j], terms)

    if s.check() == sat:
        model = s.model()
        X_rec = np.array([[model[X[i][j]].as_long() for j in range(k)] for i in range(m)])
        Y_rec = np.array([[model[Y[i][j]].as_long() for j in range(n)] for i in range(k)])
        return X_rec, Y_rec
    else:
        return None, None
