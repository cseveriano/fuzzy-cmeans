import random as rnd
import math
import matplotlib.pyplot as plt
import numpy as np


def distancia(x,y):
    dist = [(a - b) ** 2 for a, b in zip(x, y)]
    return math.sqrt(sum(dist))

def c_means(k,dados):
    fig = plt.figure(figsize=(15, 15))

    # Os centroides são escolhidos a partir de pontos aleatorios da base
    centroides = [dados[rnd.randint(0, len(dados))] for kk in range(0, k)]
    plt.scatter([xx[0] for xx in centroides],
                [xx[1] for xx in centroides],
                marker="+", s=150, color="black")

    grupos = [-1 for x in range(0, len(dados))]

    it_semmodificacao = 0

    #para cada instância
    iteracoes = 0

    while iteracoes < 1000 and it_semmodificacao < 10:
        inst_count = 0

        modificacao = False

        new_groups = [-1 for x in range(0, len(dados))]

        for instancia in dados:

            # verifica a distância para cada centroide
            grupo_count = 0

            grupotmp = grupos[inst_count]

            dists = []

            for grupo in centroides:
                dists.append(distancia(instancia, grupo))

            min_dist_index = np.argmin(dists)
            new_groups[inst_count] = min_dist_index


            inst_count = inst_count + 1

        if new_groups != grupos:
            modificacao = True
            grupos = new_groups

        if not modificacao:
            it_semmodificacao = it_semmodificacao + 1
        else:
            it_semmodificacao = 0

        # atualiza cada centroide com base nos valores médios de todas as instâncias à ela associadas
        grupo_count = 0
        for c in range(0, len(centroides)):
            grupo = [dados[kk] for kk in range(0, len(dados)) if grupos[kk] == c]
            centroides[c] = np.mean(grupo, axis=0)

        iteracoes = iteracoes + 1

    result = [centroides, grupos]

    cores = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    plt.scatter([xx[0] for xx in dados], [xx[1] for xx in dados],
                color=[cores[xx % 7] for xx in grupos], marker="o")
    plt.scatter([xx[0] for xx in centroides],
                [xx[1] for xx in centroides],
                marker="^", s=100, color="black")

    plt.show()
    print(iteracoes, it_semmodificacao)

    return result
