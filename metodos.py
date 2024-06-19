import pandas as pd
import solucao as sol


class Disciplina:
    """Classe que representa um disciplina"""
    def __init__(self, curso, periodo, sigla, ch, prof):
        self.curso = curso
        self.periodo = periodo
        self.sigla = sigla
        self.ch = ch
        self.prof = prof
        self.cor = None
        self.conflitos = []


def ler_disciplinas(arquivo):
    """Cria a lista de disciplinas a partir do arquivo de dados"""
    materias = []
    with open(arquivo, 'r') as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(',')
            try:
                ch = int(dados[3])
            except ValueError:
                print(f'Erro: {dados[3]} não é uma carga horária válida.')
                continue
            materia = Disciplina(dados[0], dados[1], dados[2], ch, dados[4])
            materias.append(materia)
    return materias


def escrever_solucao(arquivo, solucao):
    """Gera o arquivo csv com o resultado da alocação de horários"""
    with open(arquivo, 'w') as f:
        for horario, dias in enumerate(solucao):
            for dia, disciplinas in enumerate(dias):
                for disciplina in disciplinas:
                    f.write(f"{disciplina.curso}{disciplina.periodo},{dia + 1},{horario + 1},{disciplina.prof},"
                            f"{disciplina.sigla}\n")


def converter_excel_csv(arquivo_excel, nome_planilha, nome_csv):
    """Converte os dados da planilha para um arquivo csv"""
    # Ler o arquivo Excel
    df = pd.read_excel(arquivo_excel, sheet_name=nome_planilha)
    # Escrever em um arquivo CSV
    df.to_csv(nome_csv, index=False)


def aloca_solucao(disciplinas):
    """Aloca todas as disciplinas e imprime o resultado da alocação"""
    qtd_alocada = 0
    solucao = 0
    while qtd_alocada != 304:
        qtd_alocada = 0
        solucao, f_obj = sol.construir_solucao(disciplinas, 0.2)
        for dia in range(5):
            for hora in range(14):
                qtd_alocada += len(solucao[hora][dia])

    # Imprime solução encontrada
    for dia in range(5):
        print(f'\n\n\tDIA {dia+1}')
        for hora in range(14):
            print(f'\n\tHorário {hora + 1}: ')
            for disciplina in solucao[hora][dia]:
                print(f'{disciplina.sigla}')

    print(f'\nAulas alocadas: {qtd_alocada}/304')
    return solucao
