import sys
from decimal import Decimal
A, B = map(str, sys.stdin.readline().split())
A, B = Decimal(A), Decimal(B)
c = Decimal("299792458")
ret = (A + B) / (1 + (A * B) / (c * c))
print("%.10f"%ret)
