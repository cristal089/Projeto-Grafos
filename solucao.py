import random

# Parâmetros da tabela-horário
dias = list(range(5))
# São considerados 14 horários, excluindo o horário das 22h40 às 23h30
horarios_por_dia = list(range(15))


def gera_candidatos(disciplina, alpha, tabela_horario):
    """Gera horários candidatos à alocação da disciplina seguindo as restrições pertinentes"""
    candidatos = []
    # Lista os horários válidos a depender da carga horária da disciplina (dois créditos ou três créditos)
    hvalidos_cco_ch2 = [0, 1, 3, 5, 7]
    hvalidos_cco_ch3 = [0, 2, 5, 7]

    hvalidos_sin_ch2 = [10, 12]
    hvalidos_sin_ch3 = [10]

    hvalidos_opt_ch2 = hvalidos_cco_ch2 + hvalidos_sin_ch2
    hvalidos_opt_ch3 = hvalidos_cco_ch3 + hvalidos_sin_ch3

    for dia in dias:
        for horario in horarios_por_dia:
            if disciplina.curso == 'CCO':
                if disciplina.ch == 3 and horario not in hvalidos_cco_ch3:
                    continue
                if (disciplina.ch == 2 or disciplina.ch == 4) and horario not in hvalidos_cco_ch2:
                    continue                
                custo = calcular_custo(tabela_horario, disciplina, dia, horario)
                if custo >= 5000:
                    continue
                candidatos.append(((horario, dia), custo))
            
            if disciplina.curso == 'SIN':
                if disciplina.ch == 3 and horario not in hvalidos_sin_ch3:
                    continue
                if (disciplina.ch == 2 or disciplina.ch == 4) and horario not in hvalidos_sin_ch2:
                    continue                
                custo = calcular_custo(tabela_horario, disciplina, dia, horario)
                if custo >= 5000:
                    continue
                candidatos.append(((horario, dia), custo))

            if disciplina.periodo == '11' or disciplina.periodo == '12':
                if disciplina.ch == 3 and horario not in hvalidos_opt_ch3:
                    continue
                if (disciplina.ch == 2 or disciplina.ch == 4) and horario not in hvalidos_opt_ch2:
                    continue
                custo = calcular_custo(tabela_horario, disciplina, dia, horario)
                if custo >= 5000:
                    continue
                candidatos.append(((horario, dia), custo))

    candidatos.sort(key=lambda x: x[1])

    if not candidatos:
        print(f'Não foi possível alocar a disciplina {disciplina.sigla}')
        return []

    c_min = candidatos[0][1]
    c_max = candidatos[-1][1]
    limite = c_min + alpha * (c_max - c_min)

    # Define a lista de candidatos restritos
    lcr = [[c, custo] for c, custo in candidatos if custo <= limite]

    escolha = random.choice(lcr)

    return escolha


def construir_solucao(disciplinas, alpha):
    """Constrói uma solução para o problema de alocação de horários"""
    # Inicialização da tabela horário (matriz[horário][dia])
    tabela_horario = [[[] for _ in dias] for _ in horarios_por_dia]

    # Ordena as disciplinas em ordem decrescente de quantidade de conflitos
    discip_ordenadas = sorted(disciplinas, key=lambda x: len(x.conflitos), reverse=True)

    # Criação da variável que armazena o custo da solução (função objetivo)
    f_objetivo = 0
    
    while discip_ordenadas:
        disciplina = discip_ordenadas.pop(0)
        
        escolha1 = gera_candidatos(disciplina, alpha, tabela_horario)

        if not escolha1:
            continue

        horario, dia = escolha1[0]

        # Aloca a disciplina na posição escolhida da tabela-horário
        tabela_horario[horario][dia].append(disciplina)
        tabela_horario[horario + 1][dia].append(disciplina)

        if disciplina.ch == 3:
            tabela_horario[horario + 2][dia].append(disciplina)

        if disciplina.ch == 4:
            escolha2 = gera_candidatos(disciplina, alpha, tabela_horario)

            if not escolha2:
                tabela_horario[horario][dia].remove(disciplina)
                tabela_horario[horario + 1][dia].remove(disciplina)
                continue    
            
            horario2, dia2 = escolha2[0]
            tabela_horario[horario2][dia2].append(disciplina)
            tabela_horario[horario2 + 1][dia2].append(disciplina)
            f_objetivo += escolha2[1]

        # Incrementar o valor da função objetivo da solução
        f_objetivo += escolha1[1]

    return tabela_horario, f_objetivo


def calcular_custo(tabela_horario, disciplina, dia, horario):
    """Com base nas restrições, calcula o custo de alocação da disciplina em determinado horário"""
    custo = 0
    # RFT02: Diferentes períodos e professores em horários diferentes
    if disciplina.ch == 3:
        for i in range(3):
            for discip_concorrente in tabela_horario[horario + i][dia]:
                if discip_concorrente.prof == disciplina.prof or discip_concorrente.periodo == disciplina.periodo:
                    custo += 5000

    if disciplina.ch == 2 or disciplina.ch == 4:
        for i in range(2):
            for discip_concorrente in tabela_horario[horario + i][dia]:
                if discip_concorrente.prof == disciplina.prof or discip_concorrente.periodo == disciplina.periodo:
                    custo += 5000

    # RFT03: Aulas da mesma disciplina devem estar em horários adjacentes
    # Resolvido no código

    # RFT04: No máximo duas aulas da mesma disciplina por dia
    aulas_no_dia = 0    
    for h in horarios_por_dia:
        for discip in tabela_horario[h][dia]:
            if discip.sigla == disciplina.sigla:
                aulas_no_dia += 1
    if aulas_no_dia >= 2:
        custo += 5000

    # RFT05: Professor não pode lecionar mais de 6 aulas por dia
    aulas_prof_dia = 0
    for h in horarios_por_dia:
        for discip in tabela_horario[h][dia]:
            if discip.prof == disciplina.prof:
                aulas_prof_dia += 1
    if aulas_prof_dia > 6:
        custo += 5000

    # RFC01: O horário 1 (7:00) deve ser evitado. Cada aula alocada neste horário é contada como uma violação.
    if horario == 0:
        custo += 10

    return custo
