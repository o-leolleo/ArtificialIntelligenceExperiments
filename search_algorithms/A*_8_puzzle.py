from __future__ import print_function
import sys,copy,random
from heapq import heappush, heappop
from collections import deque

"""
    Problem solving agent implementation:

        it actually solves the 8x8 puzzle problem:

        given a grid like 

        1 2 3
        4   5
        6 7 8

        transform it into another given grid pattern
        by moving the empty cell optmally

        performance measure: number of steps
        
    obs.: I think I actually complicated the things a bit, 
    hope this works :)

    @author leolleo
"""

explored  = set()   # states history
parent    = dict()  # parent vector 
dist      = dict()
final_pos = dict()

# tricks 
dr = [1, -1, 0, 0]
dc = [0, 0, 1, -1]

"""
    if the grid is 
    
    a b c
    d e f
    g h i

    the returned value will be

    value = a * 10**0 + b * 10**1 + .. + i * 10**8
"""


def print_table(table):
    for i in range(3):
        for j in range(3):
	    if (table[i][j] != 9):
	        print(table[i][j],end="")
	    else:
	    	print(" ", end="")
	    print(" ", end="")
	print("")

    print("\n", end="")
	    

def hash(state):
    """ translate a grid into a number """
    value = 0

    for i in range (3):
        for j in range (3):
            value = value + 10**(3*i + j) * state[i][j]

    return value

def _hash(value):
    """ translate number into a grid """

    state = [[0 for i in range(3)] for j in range(3)]

    for i in reversed(range(3)):
        for j in reversed(range(3)):
            state[i][j] = value / 10 ** (3 * i + j)
            value = value % 10 ** (3 * i + j)

    return state
            
def get_void(state):
    for i in range(3):
        for j in range(3):
            if (state[i][j] == 9):
                return (i, j)
            

def swap_pos(r1, c1, r2, c2, state):
    state[r1][c1], state[r2][c2] = state[r2][c2], state[r1][c1]

def make_final_pos(desired):
    for i in range(3):
        for j in range(3):
                final_pos[desired[i][j]] = (i, j)

def heuristic(state):
    total = 0

    for i in range(3):
        for j in range(3):
            total = total + abs(i - final_pos[state[i][j]][0]) + abs(j - final_pos[state[i][j]][1])

    return total

def random_table(mov):
    state = [[(3*i + j + 1) for j in range(3)] for i in range(3)]

    random.seed()

    while (mov):
        pos = get_void(state) 
        k = random.randint(0, 3)

        while (pos[0] + dr[k] < 0 or pos[0] + dr[k] >= 3 or pos[1] + dc[k] < 0 or pos[1] + dc[k] >= 3):
            k = random.randint(0, 3)

        swap_pos(pos[0], pos[1], pos[0] + dr[k], pos[1] + dc[k], state) 
        mov = mov - 1

    return copy.deepcopy(state)


def A_star(state, desired):
    pq = [] 
    heappush(pq,(0,hash(state)))
    dist[hash(state)] = 0
    solved = False
    parent[hash(state)] = -1

    while (not len(pq) == 0 and not solved):
        u = heappop(pq)
        u = (u[0], _hash(u[1]))

        if (u[0] - heuristic(u[1]) > dist[hash(u[1])]): continue

        for k in range(4):
            pos = get_void(u[1])
            i = pos[0] + dr[k]
            j = pos[1] + dc[k]

            if (i >= 0 and i < 3 and j >= 0 and j < 3):
                v = copy.deepcopy(u)
                swap_pos(pos[0], pos[1], i, j, v[1])

                D = 99999999999 

                if (hash(v[1]) in dist):
                    D = dist[hash(v[1])]

                if (dist[hash(u[1])] + 1 < D):
                    parent[hash(v[1])] = hash(u[1])
                    dist[hash(v[1])] = dist[hash(u[1])] + 1

                    if (hash(v[1]) == hash(desired)):
                        solved = True
                        break

                    heappush(pq, (dist[hash(u[1])] + 1 + heuristic(v[1]), hash(v[1])))
    return solved
			
def print_solution(x):
    if (x < 0): return
    print_solution(parent[x])
    print_table(_hash(x))

state   = [ 
            [8,6,7],
            [2,5,4],
            [3,9,1]
          ]

#state = random_table(100)

desired = [
            [1,2,3],
            [4,5,6],
            [7,8,9]
          ]

make_final_pos(desired)

if (A_star(state,desired) == True):
    print_solution(hash(desired))
    print ("steps to solve: ", dist[hash(desired)])
else:
    print("doesn't have solution")

