# Non-Divisible Subset
#
# https://medium.com/@mrunankmistry52/non-divisible-subset-problem-comprehensive-explanation-c878a752f057
#
# Complete the 'nonDivisibleSubset' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY s
#


import math
import os
import random
import re
import sys

def nonDivisibleSubset(k, s):
    count = [0] * k

    for i in s:
        remainder = i % k
        count[remainder] +=1
    
    ans = min( count[0] , 1)          # Handling case 1 

    if k % 2 == 0:                    # Handling case even exception case
        ans += min(count[k//2] ,1 )

    for i in range( 1 , k//2 + 1):    # Check for the pairs and take appropriate count
        if i != k - i:           # Avoid over-counting when k is even
            ans += max(count[i] , count[k-i])
    return ans

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    k = int(first_multiple_input[1])

    s = list(map(int, input().rstrip().split()))

    result = nonDivisibleSubset(k, s)

    fptr.write(str(result) + '\n')

    fptr.close()

################################################################
################################################################
################################################################

# Queen's Attack II 
# Complete the 'queensAttack' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER k
#  3. INTEGER r_q
#  4. INTEGER c_q
#  5. 2D_INTEGER_ARRAY obstacles


# Two Solutions 

# First Solutions
def move_queen(n, updated_row, updated_col, r , c, obstacles):
    p = 0
    while True:
        r = updated_row(r)
        c = updated_col(c)
        key = (r - 1) * n + c
        if (c < 1 or c > n or r < 1 or r > n) or (key in obstacles):
            return p
        p += 1
    return p

# Complete the queensAttack function below.
def queensAttack(n, k, r_q, c_q, obs):
    obstacles = {}
    for b in obs:
        obstacles[(b[0] - 1) * n + b[1]] = None

    p = 0
    dr = [-1, -1, -1, 0, 0 , 1 , 1,1]
    dc = [0, -1, 1, 1, -1 , 0 , 1,-1]
    
    for i in range(8):
        p += move_queen(n, (lambda r: r + dr[i]), (lambda c: c + dc[i] ), r_q, c_q, obstacles)

    return p



#Second Solution
# https://www.kindsonthegenius.com/queen-attack-ii-simple-solution-hackerrank/
#
def getCellsQueenCanAttack(queenX, queenY, boardSize):
    orthognals =  2 * boardSize - 2
    diagonals = 2 * boardSize - 2 - abs(queenX - queenY) - abs(queenX + queenY - boardSize - 1)
    return orthognals + diagonals

def getRelativeLocation(queenX, queenY, pawnX, pawnY):
    if pawnY == queenY and pawnX < queenX:
        return 'L'
    if pawnY == queenY and pawnX > queenX:
        return 'R'
    if queenX == pawnX and pawnY > queenY:
        return 'U'
    if queenX == pawnX and pawnY < queenY:
        return 'D'
    if abs(queenX - pawnX) == abs(queenY - pawnY): #filter out irrelevant pawns
        if pawnY > queenY and pawnX < queenX:
            return 'UL'
        if pawnY > queenY and pawnX > queenX:
            return 'UR'
        if pawnY < queenY and pawnX > queenX:
            return 'DR'
        if pawnY < queenY and pawnX < queenX:
            return 'DL'
        
def getCellsBlockedByPawns(queenX, queenY, pawns):
    blockedCells = set()   
    for pawn in pawns:
        x = pawn[1]
        y = pawn[0]
        position = getRelativeLocation(queenX, queenY, x, y)
        if position == 'U':
            for i in range(y, n+1):
                blockedCells.add((i, x))
        if position == 'D':
            for i in range(y, 0, -1):
                blockedCells.add((i, x))
        if position == 'L':
            for i in range(x, 0, -1):
                blockedCells.add((y, i))
        if position == 'R':
            for i in range(x, n+1):
                blockedCells.add((y, i))   
        if position == 'UL':
            while y <= n and x > 0:
                blockedCells.add((y, x))
                x -= 1
                y += 1   
        if position == 'UR':
            while y <= n and x <= n:
                blockedCells.add((y, x))
                x += 1
                y += 1 
        if position == 'DR':
            while y > 0 and x <= n:
                blockedCells.add((y, x))
                x += 1
                y -= 1   
        if position == 'DL':
            while y > 0 and x > 0:
                blockedCells.add((y, x))
                x -= 1
                y -= 1 
    return len(blockedCells)

    
def queensAttack(boardSize, k, queenY, queenX, pawns):
    # Write your code here
    if len(pawns) == 0:
        return getCellsQueenCanAttack(queenX, queenY, boardSize)
    else:
        queenCells = getCellsQueenCanAttack(queenX, queenY, boardSize)
        pawnCells = getCellsBlockedByPawns(queenX, queenY, pawns)
        return queenCells - pawnCells

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    k = int(first_multiple_input[1])

    second_multiple_input = input().rstrip().split()

    r_q = int(second_multiple_input[0])

    c_q = int(second_multiple_input[1])

    obstacles = []

    for _ in range(k):
        obstacles.append(list(map(int, input().rstrip().split())))

    result = queensAttack(n, k, r_q, c_q, obstacles)

    fptr.write(str(result) + '\n')

    fptr.close()

################################################################
################################################################
################################################################