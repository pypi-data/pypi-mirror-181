#Second Solution
# https://www.kindsonthegenius.com/queen-attack-ii-simple-solution-hackerrank/
#

import math
import os
import random
import re
import sys

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