import random

# Parâmetros da tabela-horário
dias = list(range(5))
# São considerados 14 horários, excluindo o horário das 22h40 às 23h30
horarios_por_dia = list(range(15))

def gera_candidatos(disciplina, alpha, tabela_horario):
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

            if (disciplina.periodo == '11' or disciplina.periodo == '12'):
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
        
        escolha1 = gera_candidatos(disciplina, alpha, tabela_horario)

        if not escolha1:
            continue

        horario, dia = escolha1[0]

        # Aloca a disciplina na posição escolhida da tabela-horário
        tabela_horario[horario][dia].append(disciplina)
        tabela_horario[horario + 1][dia].append(disciplina)

        if(disciplina.ch == 3):
            tabela_horario[horario + 2][dia].append(disciplina)

        if(disciplina.ch == 4):
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

    # RFC01: O horário 0 (7:00) deve ser evitado. Cada aula alocada neste horário é contada como uma violação.
    if horario == 0:
        custo += 10

    # RFC02: deve-se evitar que aulas da mesma disciplina sejam alocadas em dias consecutivos.
    # if dia > 0:
    #     if disciplina.sigla in tabela_horario[horario][dia - 1]:
    #         custo += 10

    # if dia < len(tabela_horario[0]) - 1:
    #     if disciplina.sigla in tabela_horario[horario][dia + 1]:
    #         custo += 10

    # RFC03: Deve-se evitar que duas aulas da mesma disciplina sejam alocadas nos horários 5 e 6 (separadas pelo almoço)
    # Resolvido no código

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
