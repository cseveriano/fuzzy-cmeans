import random as rnd
import math
import matplotlib.pyplot as plt
import numpy as np


def distancia(x,y):
    dist = [(a - b) ** 2 for a, b in zip(x, y)]
    return math.sqrt(sum(dist))


def plot_cluster (dados, centroides, perts) :

    cores = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    fig = plt.figure(figsize=(15, 15))

    plt.scatter([xx[0] for xx in dados],[xx[1] for xx in dados],color=[cor(p) for p in perts], marker="o")
    plt.scatter([xx[0] for xx in centroides], [xx[1] for xx in centroides], marker="^",color="black",s=150)

    plt.show()

def cor(pert):
    cores = ['b','g','r','c','m','y','k']
    max_pert = max(pert)
    return cores[pert.index(max_pert)%7]

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

        # atualiza cada centroide com base nos valores médios de todas as instâncias a ele associadas
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


def calcula_pertinencia(dist_inst_c, dists, m):

    # Se a instancia é proprio centroide, sua pertinencia é de 1 para o grupo em questao e 0 para os demais

    # Instancia é o centroide do grupo avaliado
    if dist_inst_c == 0:
        result = 1
    else:
        # Instancia é o centroide de outro grupo
        if any(x == 0 for x in dists) :
            result = 0
        else:
            exp = 2/(m-1)
            result = 1 / sum([(dist_inst_c / x)**exp for x in dists])

    return result


def fuzzy_c_means(k, dados, m):

    deltadist = 0.001

    # Inicializa as centróides escolhendo elementos aleatórios dos conjuntos
    centroides = [dados[rnd.randint(0, len(dados))] for kk in range(0, k)]


    # Matriz de pertinência das instâncias aos grupos.
    U = [[0 for kk in range(0, k)] for xx in range(0, len(dados))]

    alteracaomedia = 1000

    # para cada instância
    iteracoes = 0

    while iteracoes < 1000 and alteracaomedia > deltadist:

        # Contador para instancias
        i = 0
        for instancia in dados:

            dists = []

            # Calcula distâncias entre instancias e centroides
            for c in centroides:
                dists.append(distancia(instancia, c))

            # Atualiza matriz de pertinencia para a instancia com base nas distâncias
            for j in range(0,k):
                U[i][j] = calcula_pertinencia(dists[j], dists, m)

            i += 1

        # Atualiza valores centroides
        for j in range(0,len(centroides)) :

            old_centroide = centroides[j]

            pow_pert = [x[j]**m for x in U]

            a = np.sum([p * inst for p, inst in zip(pow_pert, dados)], axis=0)
            b = np.sum(pow_pert)

            centroides[j] = a / b

            alteracaomedia += distancia(old_centroide,centroides[j])

        alteracaomedia = alteracaomedia / k
#        print(alteracaomedia)

        iteracoes = iteracoes + 1

 #   print(iteracoes)
    plot_cluster(dados, centroides, U)

    return [centroides, U]
