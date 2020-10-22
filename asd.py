_INF = 1e9
def solution():
    N = int(input())
    Floyd = [[_INF for _ in range(26)] for _ in range(26)]

    for _ in range(N):
        answer = (input().split(' '))
        Floyd[ord(answer[0]) - 97][ord(answer[2]) - 97] = 1


    for k in range(26):
        for i in range(26):
            for j in range(26):
                Floyd[i][j] = min(Floyd[i][j], Floyd[i][k] + Floyd[k][j])

    M = int(input())
    for _ in range(M):
        answer = (input().split(' '))

        if Floyd[ord(answer[0]) - 97][ord(answer[2]) - 97] != _INF:
            print('T')
        else:
            print('F')

solution()