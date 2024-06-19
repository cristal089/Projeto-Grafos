import networkx as nx
from networkx.algorithms.coloring import greedy_color
import matplotlib.pyplot as plt


def construir_grafo(disciplinas):
    """Constrói o grafo representando as restrições entre disciplinas"""
    grafo = nx.Graph()
    for disciplina in disciplinas:
        grafo.add_node(disciplina.sigla, obj=disciplina)

    n = len(disciplinas)
    for i in range(n):
        for j in range(i + 1, n):
            d1 = disciplinas[i]
            d2 = disciplinas[j]
            if d1.curso != 'Optativas' and d2.curso != 'Optativas' and d1.curso != 'Poscomp' and d2.curso != 'Poscomp':
                if d1.curso == d2.curso and d1.periodo == d2.periodo:
                    grafo.add_edge(d1.sigla, d2.sigla)
                    d1.conflitos.append(d2.sigla)
                    d2.conflitos.append(d1.sigla)
                if d1.curso == d2.curso and d1.prof == d2.prof and int(d1.periodo) % 2 == 0 and int(
                        d2.periodo) % 2 == 0:
                    grafo.add_edge(d1.sigla, d2.sigla)
                    d1.conflitos.append(d2.sigla)
                    d2.conflitos.append(d1.sigla)
                if d1.curso == d2.curso and d1.prof == d2.prof and int(d1.periodo) % 2 != 0 and int(
                        d2.periodo) % 2 != 0:
                    grafo.add_edge(d1.sigla, d2.sigla)
                    d1.conflitos.append(d2.sigla)
                    d2.conflitos.append(d1.sigla)
            else:
                if d1.prof == d2.prof and int(d1.periodo) % 2 == 0 and int(d2.periodo) % 2 == 0:
                    grafo.add_edge(d1.sigla, d2.sigla)
                    d1.conflitos.append(d2.sigla)
                    d2.conflitos.append(d1.sigla)
                if d1.prof == d2.prof and int(d1.periodo) % 2 != 0 and int(d2.periodo) % 2 != 0:
                    grafo.add_edge(d1.sigla, d2.sigla)
                    d1.conflitos.append(d2.sigla)
                    d2.conflitos.append(d1.sigla)

    return grafo


def construir_matriz_adj(grafo):
    """Constrói a matriz de adjacências do grafo criado"""
    matriz_adj_esparsa = nx.adjacency_matrix(grafo)
    matriz_adj = matriz_adj_esparsa.toarray()

    return matriz_adj


def colorir_grafo(grafo):
    """Usa a função greedy_color da biblioteca networkx para atribuir uma cor a cada vértice do grafo"""
    cores = greedy_color(grafo, strategy='largest_first')
    for sigla, cor in cores.items():
        grafo.nodes[sigla]['obj'].cor = cor


def plotar_grafo(grafo):
    """Usa as bibliotecas networkx e matplotlib para plotar o grafo recebido como parâmetro"""
    pos = nx.spring_layout(grafo, k=0.25)  # Layout do grafo
    cores = [grafo.nodes[n]['obj'].cor for n in grafo.nodes]
    labels = {n: grafo.nodes[n]['obj'].sigla for n in grafo.nodes}

    plt.figure(figsize=(12, 8))
    nx.draw(grafo, pos, node_color=cores, with_labels=True, labels=labels, node_size=500, font_size=7,
            font_weight='bold', cmap=plt.cm.rainbow)
    plt.show()
