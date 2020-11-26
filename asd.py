import sys

def solution():
    while True:
        i = sys.stdin.readline()
        if not (i): break

        N, K = map(int, i.split())
        S = N

        while N // K:
            S = S + N // K
            N = N // K + N % K
        print(S)

solution()