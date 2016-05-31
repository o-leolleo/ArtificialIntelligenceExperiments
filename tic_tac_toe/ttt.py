"""
    An implementation of tic tac toe using MINIMAX algorithm

    the program implements the tic tac toe game, where the
    player play with the machine. The machine uses the MINIMAX
    algorithm to make decisions.

    @author leolleo
"""
import copy

# initial state of empty cells
state = [[' ' for j in range(3)] for i in range(3)]

# symbols used by each player
player_symbol = {0:'X', 1:'O'}

# the machine is the player number 1 (second)
machine = 1

# count visited states during minimax
state_count = 0

def minimax(state, player):
    """
    returns the best move player can do

    Args:
        param: player number
        (on this code only called with the machine)
    """
    global state_count
    best = None
    Max = float('-inf')
    state_count = 0

    for i in range(3):
        for j in range(3):
            if (state[i][j] == ' '):
                tmp = copy.deepcopy(state)
                tmp[i][j] = player_symbol[player] 
                aux = min_value(tmp, not player)

                if (aux > Max):
                    Max = aux
                    best = tmp

    return best

def max_value(state, player):
    """
    returns the best utility value for
    the player who is trying to maximize
    his utility

    Args:
        param1: current state
        param2: max player
    """
    global state_count
    state_count +=1

    if (is_final_state(state)): return utility(state, machine)
    v = float('-inf') 

    for i in range(3):
        for j in range(3):
            if (state[i][j] == ' '):
                tmp = copy.deepcopy(state)
                tmp[i][j] = player_symbol[player] 
                v = max(v, min_value(tmp, not player))

    return v

def min_value(state, player):
    """
    returns the best utility value
    for the player who is trying to minimize
    the other utility

    Args:
        param1: current state
        param2: min player
    """
    global state_count
    state_count +=1

    if (is_final_state(state)): return utility(state, machine)  
    v = float('inf')

    for i in range(3):
        for j in range(3):
            if (state[i][j] == ' '):
                tmp = copy.deepcopy(state)
                tmp[i][j] = player_symbol[player] 
                v = min(v, max_value(tmp, not player))

    return v

def is_final_state(state):
    """
    verifies if state corresponds to a final
    state, then returns true or false. ~~ messy ~~

    Args:
        param: state
    """
    for player in [0, 1]:
        final = True
        for a in range(3):
            tmp = True
            for b in range(3):
                if (state[a][b] != player_symbol[player]): 
                    tmp = False
                    break
            if (tmp): break
            elif (a == 2): final = False

        if (final): return True

        final = True
        for a in range(3):
            tmp = True
            for b in range(3):
                if (state[b][a] != player_symbol[player]): 
                    tmp = False
                    break
            if (tmp): break
            elif (a == 2): final = False

        if (final): return True

        final = True
        for a in range(3):
            if (state[a][a] != player_symbol[player]):
               final = False 

        if (final): return True

        final = True
        for a in range(3):
            if (state[a][2 - a] != player_symbol[player]):
               final = False 

        if (final): return True

    
    final = True
    for a in range(3):
        for b in range(3):
            if (state[a][b] == ' '):
                final = False

    if (final): return True

    return False

def utility(state, player):
    """
    calculate the utility value of a state
    for a given player. Is assumed that 
    state is a final state. ~~ messy ~~

    Args:
        param1: current state
        param2: current player 
    """
    for p in [0, 1]:
        final = True
        for a in range(3):
            tmp = True
            for b in range(3):
                if (state[a][b] != player_symbol[p]): 
                    tmp = False
                    break
            if (tmp): break
            elif (a == 2): final = False

        if (final): 
            if (player == p): return 1
            else: return -1

        final = True
        for a in range(3):
            tmp = True
            for b in range(3):
                if (state[b][a] != player_symbol[p]): 
                    tmp = False
                    break
            if (tmp): break
            elif (a == 2): final = False

        if (final): 
            if (player == p): return 1
            else: return -1

        final = True
        for a in range(3):
            if (state[a][a] != player_symbol[p]):
               final = False 

        if (final): 
            if (player == p): return 1
            else: return -1

        final = True
        for a in range(3):
            if (state[a][2 - a] != player_symbol[p]):
               final = False 

        if (final): 
            if (player == p): return 1
            else: return -1

    return 0

def print_state(state):
    for k in range(3):
        print(state[k][:])
    print("")

# first player
player = 0

# main loop, the game itself
while (not is_final_state(state)):
    if (not player):
        pos = input("digite a posicao: ").split()
        pos = ord(pos[0]), ord(pos[1])
        pos = pos[0] - ord('0'), pos[1] - ord('0')
        state[pos[0]][pos[1]] = player_symbol[player] 
    else:
        state = minimax(state, player)
    
    print_state(state)
    if (player): print("# of visited states: %s\n" % state_count)
    player = not player

# who won?
if (utility(state, machine) == 1):
    print("Machine Wins!")
elif (utility(state, machine) == -1):
    print("Human Wins!")
else:
    print("it's a match!")
