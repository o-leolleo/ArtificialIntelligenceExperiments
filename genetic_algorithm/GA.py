import sys, copy, random

random.seed()

def gera_primeira_populacao():
    """
        gera a primeira população 
    """
    populacao = []

    for i in range(4):
        candidate = random.randint(0, 20)

        while (candidate in populacao):
            candidate = random.randint(0, 20)

        populacao.append(candidate);

    return populacao

def utilidade(x):
    """
        função de aptidão
    """
    return x ** 2 - 3 * x + 4 

def selecao(populacao, aptidao):
    """
        função de seleção
    """
    choosen_ones = []

    for i in range(4):
        oponente1 = random.choice(populacao)
        oponente2 = random.choice(populacao)

        # só os maneiros
        choosen_ones.append(oponente1 if (aptidao(oponente1 - 10) < aptidao(oponente2 - 10)) else oponente2)

    return choosen_ones 

def crossover(X, Y):
    """
        croosover entre os cromossomos X e Y
        taxa de crossover - 60%
    """
    if (random.randint(1, 100) <= 60):
        corte = random.randrange(5)

        upper = (2**(corte+1) - 1) << (4 - corte)
        lower = 2**(5 - corte - 1) - 1 

        tmp = X
        X = (upper & Y) | (lower & X)
        Y = (upper & tmp) | (lower & Y)

    return [X, Y]

def seleciona_pais():
    """
        seleciona os 'casais' aleatoriamente
    """
    tmp = [[0 for j in range(4)] for i in range(24)]
    lines = 0

    for a in range(4):
        for b in range(4):
            if (b != a):
                for c in range(4):
                    if (c != b and c != a):
                        for d in range(4): 
                                if (d != c and d != b and d != a):
                                    tmp[lines][:] = [a, b, c, d]
                                    lines += 1

    return tmp[random.randrange(0,lines)]

def mutacao(X):
    """
        modifica um cromossomo 
        X a uma taxa de 1%
    """
    for i in range(5):
        if (random.randint(1, 100) <= 1): 
            X ^= (1 << i)

    return X

def genetic(aptidao, max_gen):
    """
        Utiliza um algoritmo
        genético para encontrar
        o máximo de aptidão
    """
    populacao = gera_primeira_populacao()
    geracao = 0    

    while (geracao < max_gen):
        print("populacao #%s: %s" % (geracao + 1, populacao))
        choosen = selecao(populacao, aptidao)
        pais = seleciona_pais()

        populacao = crossover(choosen[pais[0]], choosen[pais[1]])
        populacao += crossover(choosen[pais[2]], choosen[pais[3]])

        for i in range(4):
            populacao[i] = mutacao(populacao[i])

        geracao += 1

    return min(populacao[:]) - 10

x = genetic(utilidade, 5)

print("\n\n%-3s | %-3s" % ("x","f(x)"))
print("-----------")
print("%-3s | %-3s" % (x, utilidade(x)))
