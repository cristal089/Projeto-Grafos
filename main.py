import pandas as pd
import modelagem as mod
import leitura as le
import grasp as grasp


def main():
    arquivo_csv = 'dados.csv'                               # Leitura dos dados
    disciplinas = le.ler_disciplinas(arquivo_csv)           # Construção da lista de disciplinas
    grafo = mod.construir_grafo(disciplinas)                # Construção do grafo
    matriz_adj = mod.construir_matriz_adj(grafo)            # Obtém a matriz de adjacências do grafo
    mod.colorir_grafo(grafo)                                # Coloração do grafo
    # mod.plotar_grafo(grafo)                                 # Plotagem do grafo
    dados = pd.read_csv('dados.csv')

    solucao, f_obj = grasp.construir_solucao_inicial(disciplinas, 0.2)

    qtd = 0
    for dia in range(5):
        print(f'\n\n\tDIA {dia+1}')
        for hora in range(15):
            print(f'\n\tHorário {hora + 1}: ')
            for disciplina in solucao[hora][dia]:
                qtd += 1
                # if disciplina.periodo == '1' and disciplina.curso == 'CCO':
                print(f'{disciplina.sigla}')

    print(f'\nCUSTO DA SOLUÇÃO: {f_obj}')
    print(f'\nAulas alocadas: {qtd}/321')

    le.escrever_solucao('resultado.csv', solucao)


if __name__ == "__main__":
    main()
