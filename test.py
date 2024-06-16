import pandas as pd
import random

# Leitura do arquivo CSV
df = pd.read_csv('dados.csv')


# Estrutura para armazenar as ofertas de disciplinas
class Oferta:
    def __init__(self, curso, periodo, sigla, ch, professor):
        self.curso = curso
        self.periodo = periodo
        self.sigla = sigla
        self.ch = ch
        self.professor = professor


# Carregar dados das ofertas
ofertas = [Oferta(row['CURSO'], row['PERIODO'], row['SIGLA'], row['CH'], row['PROFESSOR']) for index, row in
           df.iterrows()]

# Inicializar a tabela-horário
dias = 5
horarios_por_dia = 16
tabela_horario = [[None for _ in range(horarios_por_dia)] for _ in range(dias)]


# Função de custo que avalia a qualidade da alocação
def calcular_custo(tab_hora, oferta, d, horario):
    custo = 0
    # RFC01: Evitar horários 1 e 11
    if horario == 1 or horario == 11:
        custo += 1

    # RFC02: Evitar aulas em dias consecutivos
    if d > 0 and tab_hora[d - 1][horario] == oferta.sigla:
        custo += 1

    # RFC03: Evitar aulas nos horários 5 e 6
    if horario == 5 or horario == 6:
        custo += 1

    return custo


# Função para verificar as restrições fortes
def verificar_restricoes_fortes(tab_horario, disciplina, dia, horario):
    # RFT01: Todas as aulas devem ser alocadas (verificado na construção da solução)
    # RFT02: Diferentes períodos e professores em horários diferentes
    for d in range(dias):
        for h in range(horarios_por_dia):
            if tab_horario[d][h] and (tab_horario[d][h].periodo == disciplina.periodo or
                                      tab_horario[d][h].professor == disciplina.professor):
                if dia == d and horario == h:
                    return False

    # RFT03: Aulas da mesma disciplina devem estar em horários adjacentes
    if dia > 0 and tab_horario[dia - 1][horario] == disciplina.sigla:
        return True
    if dia < dias - 1 and tab_horario[dia + 1][horario] == disciplina.sigla:
        return True

    # RFT04: No máximo duas aulas da mesma disciplina por dia
    aulas_no_dia = sum(1 for h in range(horarios_por_dia) if tab_horario[dia][h] == disciplina.sigla)
    if aulas_no_dia >= 2:
        return False

    # RFT05: Professor não pode lecionar mais de 6 aulas por dia
    aulas_do_professor_no_dia = sum(1 for h in range(horarios_por_dia) if
                                    tab_horario[dia][h] and tab_horario[dia][h].professor == disciplina.professor)
    if aulas_do_professor_no_dia >= 6:
        return False

    return True


# Função para construir a solução inicial
def construir_solucao_inicial(ofertas, tabela_horario, alpha):
    # Ordena as ofertas pelo número de horários possíveis (simplificado para o exemplo)
    ofertas_ordenadas = sorted(ofertas, key=lambda oferta: oferta.ch)

    while ofertas_ordenadas:
        oferta = ofertas_ordenadas.pop(0)  # Remove a oferta com menos horários disponíveis
        horarios_alocados = 0
        while horarios_alocados < oferta.ch:
            LC = []
            for dia in range(dias):
                for horario in range(horarios_por_dia):
                    if (oferta.curso == 'CCO' and 1 <= horario <= 11) or (oferta.curso == 'SIN' and 12 <= horario <= 16):
                        if verificar_restricoes_fortes(tabela_horario, oferta, dia, horario):
                            custo = calcular_custo(tabela_horario, oferta, dia, horario)
                            LC.append(((dia, horario), custo))

            LC.sort(key=lambda x: x[1])  # Ordena LC pelo custo

            if not LC:
                continue  # Não foi possível alocar a oferta

            # cmin = LC[0][1]
            # cmax = LC[-1][1]
            # limite = cmin + alpha * (cmax - cmin)
            #
            # LRC = [posicao for posicao, custo in LC if custo <= limite]
            #
            # posicao_escolhida = random.choice(LRC)
            #
            # dia, horario = posicao_escolhida
            #
            # # Aloca a oferta na posição escolhida da tabela-horário
            # tabela_horario[dia][horario] = oferta
            # horarios_alocados += 1

    return tabela_horario


# Parâmetro alpha para LRC
alpha = 0.5

# Construção da solução inicial
solucao_inicial = construir_solucao_inicial(ofertas, tabela_horario, alpha)

# Impressão da solução inicial
for dia in range(dias):
    print(f"Dia {dia + 1}: {[oferta.sigla if oferta else '.' for oferta in solucao_inicial[dia]]}")
