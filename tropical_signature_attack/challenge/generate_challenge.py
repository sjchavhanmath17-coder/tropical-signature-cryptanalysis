
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from src.gms26 import keygen, sign

m, n, k = 8, 8, 7
X, Y, T = keygen()
T_list = T.tolist()
X_list = X.tolist()
Y_list = Y.tolist()

# Generate 128 signatures
Ms, As, Bs, Ps, Rs, Ss = [], [], [], [], [], []
for i in range(128):
    M = np.random.randint(0, 256, size=(n, m))
    sig = sign(M, X, Y)
    Ms.append(sig['M'].tolist())
    As.append(sig['A'].tolist())
    Bs.append(sig['B'].tolist())
    Ps.append(sig['P'].tolist())
    Rs.append(sig['R'].tolist())
    Ss.append(sig['S'].tolist())

# Write to chall.py
with open('challenge/chall.py', 'w') as f_out:
    f_out.write(f"m,n,k = {m},{n},{k}\n")
    f_out.write(f"T = {T_list}\n")
    f_out.write(f"X_true = {X_list}\n")
    f_out.write(f"Y_true = {Y_list}\n")
    for i in range(128):
        f_out.write(f"M{i} = {Ms[i]}\n")
        f_out.write(f"A{i} = {As[i]}\n")
        f_out.write(f"B{i} = {Bs[i]}\n")
        f_out.write(f"P{i} = {Ps[i]}\n")
        f_out.write(f"R{i} = {Rs[i]}\n")
        f_out.write(f"S{i} = {Ss[i]}\n")
print("challenge/chall.py generated.")
