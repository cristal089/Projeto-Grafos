import pandas as pd


class Disciplina:
    def __init__(self, curso, periodo, sigla, ch, prof):
        self.curso = curso
        self.periodo = periodo
        self.sigla = sigla
        self.ch = ch
        self.prof = prof
        self.cor = None
        self.conflitos = []


def ler_disciplinas(arquivo):
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
    with open(arquivo, 'w') as f:
        for horario, dias in enumerate(solucao):
            for dia, disciplinas in enumerate(dias):
                for disciplina in disciplinas:
                    f.write(f"{disciplina.curso}{disciplina.periodo},{dia + 1},{horario + 1},{disciplina.sigla}\n")


def converter_excel_csv(arquivo_excel, nome_planilha, nome_csv):
    # Ler o arquivo Excel
    df = pd.read_excel(arquivo_excel, sheet_name=nome_planilha)
    # Escrever em um arquivo CSV
    df.to_csv(nome_csv, index=False)
