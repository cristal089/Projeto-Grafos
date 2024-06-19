import modelagem as mod
import metodos as met


def main():

    arquivo_csv = 'dados.csv'                               # Leitura dos dados

    disciplinas = met.ler_disciplinas(arquivo_csv)          # Construção da lista de disciplinas

    grafo = mod.construir_grafo(disciplinas)                # Construção do grafo

    mod.colorir_grafo(grafo)                                # Coloração do grafo

    mod.plotar_grafo(grafo)                                 # Plotagem do grafo

    solucao = met.aloca_solucao(disciplinas)                # Gera e imprime a solução gerada

    met.escrever_solucao('resultado.csv', solucao)   # Cria o arquivo csv com o resultado da alocação de horários


if __name__ == "__main__":
    main()
