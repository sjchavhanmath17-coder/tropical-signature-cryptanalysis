
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import time
from src.gms26 import keygen, sign
from src.attacks.key_recovery import recover_from_signatures

m, n, k = 8, 8, 7
MAX_VAL = 255
TRIALS = 100                # as in your paper
TIMEOUT = 60                # solver timeout in seconds (safety)

# Warm-up: run a small instance to load Z3 and compile constraints
print("Warming up...")
X_w, Y_w, T_w = keygen()
M_w = np.random.randint(0, MAX_VAL+1, size=(n, m))
sig_w = sign(M_w, X_w, Y_w)
_ = recover_from_signatures([sig_w], T_w, dims=(m,n,k), max_val=MAX_VAL, timeout=5)

def run_experiment(N, trials=TRIALS):
    success = 0
    times_success = []
    times_all = []
    for _ in range(trials):
        X, Y, T = keygen()
        sigs = []
        for _ in range(N):
            M = np.random.randint(0, MAX_VAL+1, size=(n, m))
            sigs.append(sign(M, X, Y))
        start = time.time()
        Xr, Yr = recover_from_signatures(sigs, T, dims=(m,n,k), max_val=MAX_VAL, timeout=TIMEOUT)
        elapsed = time.time() - start
        times_all.append(elapsed)
        if Xr is not None:
            # Verify recovered key reproduces T
            Tr = np.array([[min(Xr[i,l] + Yr[l,j] for l in range(k)) for j in range(n)] for i in range(m)])
            if np.array_equal(T, Tr):
                success += 1
                times_success.append(elapsed)
    rate = success / trials
    avg_succ = np.mean(times_success) if times_success else float('nan')
    avg_all = np.mean(times_all)
    return rate, avg_succ, avg_all

print("\nRunning experiments...")
results = {}
for N in [1,2,3,4]:
    rate, avg_succ, avg_all = run_experiment(N)
    results[N] = (rate, avg_succ, avg_all)

print("\n" + "="*50)
print("Hardware: Google Colab, Intel Xeon CPU @ 2.20GHz")
print("="*50)
print("\n=== Results ===")
print("N | Success rate | Avg time (success) | Avg time (all)")
print("---|--------------|--------------------|---------------")
for N in [1,2,3,4]:
    rate, avg_succ, avg_all = results[N]
    print(f"{N}  | {rate*100:6.1f}%      | {avg_succ:6.2f} s           | {avg_all:6.2f} s")
