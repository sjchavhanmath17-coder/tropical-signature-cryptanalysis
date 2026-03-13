
from z3 import Or

def add_min(s, c, terms):
    c_int = int(c)
    for t in terms:
        s.add(c_int <= t)
    s.add(Or([c_int == t for t in terms]))
