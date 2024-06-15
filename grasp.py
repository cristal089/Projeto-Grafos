import random

# Parâmetros da tabela-horário
dias = list(range(5))
horarios_por_dia = list(range(15))


def construir_solucao_inicial(disciplinas, alpha):
    """Constrói uma solução inicial de maneira gulosa, mas introduzindo um elemento de aleatoriedade para evitar ficar
    preso em ótimos locais"""
    # Inicialização da tabela horário (matriz[horário][dia])
    tabela_horario = [[[] for _ in dias] for _ in horarios_por_dia]

    # Ordena as disciplinas em ordem decrescente de quantidade de conflitos
    discip_ordenadas = sorted(disciplinas, key=lambda x: len(x.conflitos), reverse=True)

    # Criação da variável que armazena o custo da solução (função objetivo)
    f_objetivo = 0
    while discip_ordenadas:
        disciplina = discip_ordenadas.pop(0)
        horarios_alocados = 0
        while horarios_alocados < disciplina.ch:
            candidatos = []
            for dia in dias:
                for horario in horarios_por_dia:
                    if ((disciplina.curso == 'CCO' and 0 <= horario < 10) or
                            (disciplina.curso == 'SIN' and 10 <= horario < 15) or
                            (disciplina.periodo == '11' or disciplina.periodo == '12')):
                        custo = calcular_custo(tabela_horario, disciplina, dia, horario)
                        candidatos.append(((horario, dia), custo))

            candidatos.sort(key=lambda x: x[1])

            if not candidatos:
                print(f'Não foi possível alocar a disciplina {disciplina.sigla}')
                continue

            c_min = candidatos[0][1]
            c_max = candidatos[-1][1]
            limite = c_min + alpha * (c_max - c_min)

            # Define a lista de candidatos restritos
            lcr = [[c, custo] for c, custo in candidatos if custo <= limite]

            escolha = random.choice(lcr)
            horario, dia = escolha[0]

            # Incrementar o valor da função objetivo da solução
            f_objetivo += escolha[1]

            # Aloca a disciplina na posição escolhida da tabela-horário
            tabela_horario[horario][dia].append(disciplina)
            horarios_alocados += 1

    return tabela_horario, f_objetivo


def calcular_custo(tabela_horario, disciplina, dia, horario):
    """Com base nas restrições, calcula o custo de alocação da disciplina em determinado horário"""
    custo = 0
    # RFT02: Diferentes períodos e professores em horários diferentes
    for d in dias:
        for h in horarios_por_dia:
            for discip in tabela_horario[h][d]:
                if discip.periodo == disciplina.periodo or discip.prof == disciplina.prof:
                    if dia == d and horario == h:
                        custo += 5000

    # # RFT03: Aulas da mesma disciplina devem estar em horários adjacentes
    adj = False
    if horario > 0 and disciplina in tabela_horario[horario - 1][dia]:
        adj = True
    if horario < horarios_por_dia[-1] and disciplina in tabela_horario[horario + 1][dia]:
        adj = True
    if not adj:
        custo += 5000

    # RFT04: No máximo duas aulas da mesma disciplina por dia
    aulas_no_dia = 0
    for h in horarios_por_dia:
        for discip in tabela_horario[h][dia]:
            if discip.sigla == disciplina.sigla:
                aulas_no_dia += 1
    if aulas_no_dia > 2:
        custo += 5000

    # RFT05: Professor não pode lecionar mais de 6 aulas por dia
    aulas_prof_dia = 0
    for h in horarios_por_dia:
        for discip in tabela_horario[h][dia]:
            if discip.prof == disciplina.prof:
                aulas_prof_dia += 1
    if aulas_prof_dia > 6:
        custo += 5000

    # RFC01: O horário 1 deve ser evitado. Cada aula alocada neste horário é contada como uma violação.
    if horario == 1:
        custo += 10

    # RFC02: deve-se evitar que aulas da mesma disciplina sejam alocadas em dias consecutivos.
    if dia > 0:
        if disciplina.sigla in tabela_horario[horario][dia - 1]:
            custo += 10

    if dia < len(tabela_horario[0]) - 1:
        if disciplina.sigla in tabela_horario[horario][dia + 1]:
            custo += 10

    # RFC03: Deve-se evitar que duas aulas da mesma disciplina sejam alocadas nos horários 5 e 6 (separadas pelo almoço)
    if horario == 5 or horario == 6:
        for d in range(len(tabela_horario[0])):
            if disciplina.sigla in tabela_horario[5][d] and disciplina.sigla in tabela_horario[6][d]:
                custo += 10

    return custo


# def custo_solucao(tabela):
#     custo = 0
#     for horario in tabela[0]:
#         for dia in tabela[1]:
#             if



def busca_local(solucao, custo):
    """Melhora a solução inicial.
    Realiza uma busca local na vizinhança da solução atual para tentar encontrar uma solução melhor"""
    # Faz uma cópia da solução atual
    melhor_solucao = solucao

    for i in range(len(solucao)):
        for j in range(i + 1, len(solucao)):
            # Troca os elementos i e j da solução numa tentativa de melhorá-la
            solucao[i], solucao[j] = solucao[j], solucao[i]
            # Calcula o custo da solução após a troca
            custo_atual = sum(custo[i] for i in solucao)

            if custo_atual < custo:
                # Se o custo for menor, atualiza o melhor custo para o custo da solução após a troca
                melhor_custo = custo_atual
                # Também atualiza a melhor solução para a solução após a troca
                melhor_solucao = solucao.copy()
            # Troca novamente os elementos i e j da solução para restaurar a ordem original
            solucao[i], solucao[j] = solucao[j], solucao[i]

    # Retorna a melhor solução encontrada
    return melhor_solucao


def grasp(disciplinas, alpha, max_iter):
    """Implementa o algoritmo GRASP"""
    # Inicializa a melhor solução com None
    melhor_solucao = None
    # Inicializa o melhor custo com infinito
    melhor_custo = float('inf')

    # Inicia um loop que será executado max_iter vezes
    for _ in range(max_iter):
        # Constrói uma solução usando a função construcao_gulosa_aleatoria
        solucao = construir_solucao_inicial(disciplinas, alpha)
        # Melhora a solução usando a função busca_local
        solucao = busca_local(solucao, disciplinas)
        # Calcula o custo da solução
        custo_solucao = sum(disciplinas[i] for i in solucao)
        #  Verifica se o custo da solução é menor que o melhor custo encontrado até agora
        if custo_solucao < melhor_custo:
            # Se a condição acima for verdadeira, atualiza o melhor custo para o custo da solução
            melhor_custo = custo_solucao
            # Também atualiza a melhor solução para a solução atual
            melhor_solucao = solucao

    # Retorna a melhor solução encontrada
    return melhor_solucao
