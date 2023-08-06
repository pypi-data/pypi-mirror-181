import igraph
import random
import numpy as np
import math
import collections
from graphcol.gulosos import Gulosos

class Metaheuristicas:
    """
    Classe com funções que executam algoritmos de coloração que usam metaheurísticas.
    """

    def tabucol(grafo, solucao_inicial=None, tabu=5, iteracoes_min=20, iteracoes_max=50, cores_max = None, iteracoes_s_mudanca = 10, msg_print = True):
        """
        Função usada para devolver uma coloração do grafo passado como parâmetro
        usando o algoritmo Coloração Tabu. A função realiza uma exploração do espaço de soluções
        impróprio e devolve a primeira melhor solução viável encontrada. Caso não seja encontrada solução
        viável com os parâmetros passados será retornada uma mensagem indicando isso e o grafo com 
        uma coloração imprópria. 

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph
        solucao_inicial (list): Lista de inteiros que deve possuir uma coloração inicial do grafo passado.
                                Caso não seja passado uma solução aleatória será construída.
        tabu (int): Valor tabu, quantidade de iterações que um movimento permanecerá na lista tabu. O valor
                    padrão é 5.
        iteracoes_min (int): Número mínimo de iterações que o algoritmo deve realizar antes da solução ser devolvida.
        iteracoes_max (int): Número mínimo de iterações que o algoritmo pode realizar antes da solução ser devolvida.
        cores_max (int): Número de cores máximo que deve ser considerado durante a construção da solução. Caso não seja
                         passado um valor, será usada a quantidade de vértices do grafo.
        limite_melhora (int): Caso o algoritmo faça essa quantidade de iterações em sequência e não haja uma mudança
                              na quantidade de cores da solução calculada o algoritmo para a execução.
    
        Returns:
        igraph.Graph: Retorna o mesmo grafo, porém, com adição da label "cor",
        para acessá-la use grafo.vs["cor"]
        """

        if isinstance(grafo, igraph.Graph) is False:
            raise Exception("O grafo passado como parâmetro deve pertencer à classe igraph.Graph.")

        if cores_max is None:
            cores_max = grafo.vcount()
        else:
            if isinstance(cores_max, int) is False:
                raise("O parâmetro cores_max deve ser um int.") 

        def criar_solucao_inicial(grafo):
            """
            Função usada para criar uma solução inicial caso essa não seja passada na chamada da função TabuCol.
            Por ser um algoritmo que trabalha no espaço de soluções impróprias, a solução gerada aqui é totalmente
            feita de forma aleatória.
            """
            for vertice in range(grafo.vcount()):
                cor_aleatoria = random.choice(list(range(cores_max)))
                grafo.vs[vertice]["cor"] = cor_aleatoria
            return grafo
        
        if solucao_inicial is None:
            grafo = criar_solucao_inicial(grafo)
        else:
            if isinstance(solucao_inicial, list) is False:
                raise Exception("A solução inicial passada deve estar no formato de uma lista de inteiros com tamanho igual à quantidade de vértices do grafo.")
            if len(solucao_inicial) != grafo.vcount():
                raise Exception("O tamanho da lista de solução inicial deve ser igual à quantidade de vértices do grafo.")
            if all([isinstance(cor, int) for cor in solucao_inicial]) is False:
                raise Exception("Todos os elementos da solução inicial passada devem ser inteiros.")
            if max(solucao_inicial) > grafo.vcount():
                raise Exception("Na solução inicial passada não deve ter um inteiro maior que a quantidade de vértices do grafo.")
            cores_max = len(set(solucao_inicial))
            grafo.vs["cor"] = solucao_inicial

        lista_cores = list(range(cores_max))

        lista_tabu = np.zeros((grafo.vcount(), len(lista_cores)))

        def cria_lista_auxiliar(grafo):
            """
            Função que cria e atualiza a lista auxiliar usada no algoritmo de Coloração Tabu.
            Essa lista mantém a referência de quantos vértices de uma cor X são vizinhos de um vértice Y.
            """
            lista_auxiliar = np.zeros((grafo.vcount(), len(lista_cores)))
            lista_arestas = grafo.get_edgelist()
            for v_1, v_2 in lista_arestas:
                lista_auxiliar[v_1][grafo.vs["cor"][v_2]] += 1
                lista_auxiliar[v_2][grafo.vs["cor"][v_1]] += 1
            return lista_auxiliar
        lista_auxiliar = cria_lista_auxiliar(grafo)

        def cria_lista_colisoes(grafo):
            """
            Função que devolve uma lista com as colisões no grafo. Cada elemento da lista é uma 
            tupla com a aresta causadora da colisão.
            """
            lista_arestas = grafo.get_edgelist()
            colisoes = []
            for v_1, v_2 in lista_arestas:
                if grafo.vs[v_1]["cor"]==grafo.vs[v_2]["cor"]:
                    colisoes.append((v_1,v_2))
            return colisoes        
        lista_colisoes = cria_lista_colisoes(grafo)

        def movimento(grafo, lista_cores, lista_tabu, lista_auxiliar, lista_colisoes, tabu, iteracao):
            """
            Função que realiza um movimento de exploração dentro do algoritmo de Coloração Tabu.
            A função envolve selecionar um vértice para explorar soluções vizinhas relacionadas à troca de cor desse vértice,
            calcular o custo de cada movimento e verificar qual o próximo movimento.
            """
            if not lista_colisoes:
                vertice_selecionado = random.choice(list(range(grafo.vcount())))
            else:
                vertice_selecionado = random.choice(list(random.choice(lista_colisoes)))
            cor_inicial = grafo.vs[vertice_selecionado]["cor"]

            melhor_colisoes = len(lista_colisoes)
            cor_movimento = cor_inicial
            for cor in lista_cores:
                if cor != cor_inicial and lista_tabu[vertice_selecionado][cor] <= iteracao:
                    grafo.vs[vertice_selecionado]["cor"] = cor
                    colisoes = len(lista_colisoes) + lista_auxiliar[vertice_selecionado][cor] - lista_auxiliar[vertice_selecionado][cor_inicial]
                    if colisoes <= melhor_colisoes:
                        melhor_colisoes = colisoes
                        cor_movimento = cor
            if cor_movimento == cor_inicial:
                cor_movimento = random.choice(lista_cores)
            lista_tabu[vertice_selecionado][cor_inicial] = tabu + iteracao
            grafo.vs[vertice_selecionado]["cor"] = cor_movimento
            return grafo, lista_tabu

        iteracoes = 1
        melhor_coloracao = grafo.vcount()
        cores_atual = melhor_coloracao
        melhor_grafo = grafo
        cores_anterior = -1
        contador_iteracoes_iguais = 0
        if isinstance(iteracoes_min, int) is False:
            raise("O número de iterações mínimo deve ser um inteiro.")
        while(len(lista_colisoes) > 0) or (iteracoes < iteracoes_min):
            if iteracoes > iteracoes_max:
                break
            if cores_anterior == cores_atual:
                contador_iteracoes_iguais = contador_iteracoes_iguais + 1
                if contador_iteracoes_iguais == iteracoes_s_mudanca:
                    break
            else: 
                contador_iteracoes_iguais = 0
            grafo, lista_tabu = movimento(grafo, lista_cores, lista_tabu, lista_auxiliar, lista_colisoes, tabu, iteracoes)
            iteracoes += 1
            lista_colisoes = cria_lista_colisoes(grafo)
            lista_auxiliar = cria_lista_auxiliar(grafo)
            cores_anterior = cores_atual
            cores_atual = len(set(grafo.vs["cor"]))
            if cores_atual < melhor_coloracao and len(lista_colisoes) == 0:
                melhor_coloracao = cores_atual
                melhor_grafo = grafo

        if len(cria_lista_colisoes(melhor_grafo)) > 0 and msg_print == True:
            print("Não foi possível encontrar solução viável com os parâmetros passados.")      

        return melhor_grafo

    def hill_climbing(grafo, divisao = 0.75, iteracoes_max=50, iteracoes_s_melhora = 10):
        """
        Função usada para devolver uma coloração do grafo passado como parâmetro usando o algoritmo 
        Hill Climbing, algoritmos que trabalha sobre o espaço de soluções viáveis.
        Esse algoritmo divide as cores de uma solução inicial em dois grupos e tenta encontrar 
        vértices de um desses dois grupos que possa ser colorido com alguma das cores
        do primeiro grupo sem perder a viabilidade da solução. O algoritmo também tira proveito do algoritmo
        guloso para aumentar a região de exploração sem aumentar a quantidade de cores usadas a cada iteração.

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph
        divisao_inicial (float): Número entre 0 e 1 que indica qual a divisão de cores inicial que 
        será realizada. Exemplo, 0.75 indica que o algoritmo tentará tranferir os vértices de 1/4 das cores
        existentes.
        max_iteracoes (int): Critério de parada que define número máximo de iterações que o algoritmo realiza

        Returns:
        igraph.Graph: Retorna o mesmo grafo, porém, com adição da label "cor",
        para acessá-la use grafo.vs["cor"]
        """

        if isinstance(grafo, igraph.Graph) is False:
            raise Exception("O grafo passado como parâmetro deve pertencer à classe igraph.Graph.")

        def cria_tabela_viabilidade(grafo, qtd_cores, qtd_vertices):
            """
            Função que cria a tabela de viabilidade que indica se um determinado vértice tem ou 
            não vizinhos em uma cor. Devolve a tabela de viabilidade calculada onde as linhas representam
            os vértices e as colunas representam as cores. Se um vértice possui vizinhos em uma cor então 
            o valor na posição referente a essa combinação é 1, caso não é 0.
            """
            tabela_viabilidade = np.zeros((grafo.vcount(), qtd_cores))
            lista_arestas = grafo.get_edgelist()
            for vertice_1 in range(qtd_vertices):
                for vertice_2 in range(qtd_vertices):
                    if tabela_viabilidade[vertice_1][grafo.vs[vertice_2]["cor"]] == 0:
                        if (vertice_1,vertice_2) in lista_arestas or (vertice_2,vertice_1) in lista_arestas:
                            tabela_viabilidade[vertice_1][grafo.vs[vertice_2]["cor"]] = 1
            return tabela_viabilidade

        def divide_cores(qtd_cores, divisao):
            """
            Função que divide aleatoriamente as cores usadas durante a iteração do grafo em dois
            grupos visando identificar possíveis cores sendo usadas sem utilidade. Retorna os 
            dois grupos de cores em duas listas.
            """
            cores_rand = random.sample(list(range(qtd_cores)), qtd_cores)
            grupo_cores_original = cores_rand[:math.floor(qtd_cores*divisao)]
            grupo_cores_transferir = cores_rand[math.floor(qtd_cores*divisao):]
            return grupo_cores_original, grupo_cores_transferir

        def transferencias(grafo, tabela_viabilidade):
            """
            Função que avalia se existem transferências de vértices coloridos com cores do grupo 2
            que possam ser coloridos com cores do grupo 1 sem fazer a solução se tornar inviável.
            Além de avaliar essa função também realiza essas transferências.
            """
            for vertice in range(qtd_vertices):
                if grafo.vs[vertice]["cor"] in grupo_cores_2:
                    for cor in grupo_cores_1:
                        if tabela_viabilidade[vertice][cor] == 0:
                            grafo.vs[vertice]["cor"] = cor
                            vizinhanca = grafo.neighbors(vertice)
                            for vizinho in vizinhanca:
                                tabela_viabilidade[vizinho][cor] = 1
            return grafo, tabela_viabilidade
        
        def ordem_prox_iteracao(grafo, qtd_vertices):
            """
            Função que recebe o grafo da iteração atual e devolve uma lista com uma ordem dos vértices para
            ser usada na construção da solução inicial da próxima iteração. Essa construção é necessária
            pois o algoritmo aqui implementado usa o algoritmo guloso como heurística auxiliar de exploração.
            A construção dessa ordem é feita com base num teorema que garante que se a ordem passada considera
            cada cor um turno, não há como a solução devolvida ter mais cores do que a inicialmente considerada
            na hora da construção da ordem. 
            """
            cores = grafo.vs["cor"]
            vertices = list(range(qtd_vertices))
            vertices_coloridos = zip(cores, vertices)
            vertices_coloridos_ordenados = sorted(vertices_coloridos)
            ordem = [vertice for _, vertice in vertices_coloridos_ordenados]
            return ordem

        iteracao = 0
        ordem_guloso = None
        qtd_vertices = grafo.vcount()
        qtd_cores = 0
        contador_iteracoes_iguais = 0
        while iteracao <= iteracoes_max:
            cores_anterior = qtd_cores
            grafo_sol_inicial = Gulosos.guloso(grafo, ordem_guloso)
            qtd_cores = len(set(grafo_sol_inicial.vs["cor"]))
            if cores_anterior == qtd_cores:
                contador_iteracoes_iguais = contador_iteracoes_iguais + 1
                if contador_iteracoes_iguais == iteracoes_s_melhora:
                    print(f"Algoritmo não apresenta melhora de resultado há {iteracoes_s_melhora} iterações")
                    break
            else: 
                contador_iteracoes_iguais = 0
            iteracao = iteracao + 1
            tabela_viabilidade = cria_tabela_viabilidade(grafo, qtd_cores, qtd_vertices)
            grupo_cores_1, grupo_cores_2 = divide_cores(qtd_cores, divisao)
            grafo, tabela_viabilidade = transferencias(grafo, tabela_viabilidade)
            ordem_guloso = ordem_prox_iteracao(grafo, qtd_vertices)

        return grafo

    def evolucionario(grafo, n_pop = 20, iteracoes_tuning = 20):
        """
        Função usada para devolver uma coloração do grafo passado como parâmetro usando o algoritmo 
        Híbrido Evolucionário (HE), algoritmos que trabalha sobre o espaço de soluções inviáveis.
        O algoritmo recebe em sua entrada um grafo e devolve a melhor solução viável encontrada durante a exploração.
        Caso nenhuma solução viável seja encontrada é retornada uma mensagem de erro informando isso.

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph
        n_pop (int): Quantidade de elementos que a população vai manter
        iteracoes_tuning (int): Quantidade de iterações que serão realizados os processos de evolução

        Returns:
        igraph.Graph: Retorna o mesmo grafo, porém, com adição da label "cor",
        para acessá-la use grafo.vs["cor"]
        """

        if isinstance(grafo, igraph.Graph) is False:
            raise Exception("O grafo passado como parâmetro deve pertencer à classe igraph.Graph.")
        
        def criar_pop_inicial(grafo, n_pop):
          """
          Função que gera a primeira geração de indivíduos da população usada durante o algoritmo.
          Devolve uma lista com soluções
          """
          pop_solucoes = []
          for i in range(n_pop):
            solucao = Gulosos.dsatur(grafo, None).vs["cor"]
            pop_solucoes.append(solucao)
          return pop_solucoes

        def operador_recombinacao(pop_solucoes_operador, n_pop, vertices):
          """
          Função que realiza operação de recombinação de duas soluções mães, atualmente presentes na população,
          e gera uma solução filha. Aqui estamos usando o operador conhecido como Greedy Partition Crossover.
          """
          solucao_filha = [-1] * vertices
          contador_vertices_pintados = 0
          contador_cores = 0
          indices_maes = random.sample(range(n_pop), 2)
          indice_mae1 = indices_maes[0]
          indice_mae2 = indices_maes[1]
          solucao_mae1 = pop_solucoes_operador[indice_mae1].copy()
          solucao_mae2 = pop_solucoes_operador[indice_mae2].copy() 
          solucao_mae1_limpa = solucao_mae1.copy()
          solucao_mae2_limpa = solucao_mae2.copy()
          flag_mae = 0
          while contador_vertices_pintados < vertices : 
            contagem_mae1 = collections.Counter([vertice for vertice in solucao_mae1_limpa if vertice != -1])
            contagem_mae2 = collections.Counter([vertice for vertice in solucao_mae2_limpa if vertice != -1])
            cor_maior_mae1 = max(contagem_mae1, key=contagem_mae1.get)
            cor_maior_mae2 = max(contagem_mae2, key=contagem_mae2.get)
            if (flag_mae == 2) or (contagem_mae1[cor_maior_mae1] > contagem_mae2[cor_maior_mae2] and flag_mae == 0):
              flag_mae = 1
              for vertice in range(vertices):
                if (solucao_mae2[vertice] == cor_maior_mae2) and (solucao_mae1_limpa[vertice] != -1):
                  solucao_filha[vertice] = contador_cores
                  solucao_mae1_limpa[vertice] = -1
                  solucao_mae2_limpa[vertice] = -1
                  contador_vertices_pintados = contador_vertices_pintados + 1
            elif (flag_mae == 1) or (contagem_mae1[cor_maior_mae1] < contagem_mae2[cor_maior_mae2] and flag_mae == 0):
              flag_mae = 2
              for vertice in range(vertices):
                if (solucao_mae1[vertice] == cor_maior_mae1) and (solucao_mae2_limpa[vertice] != -1):
                  solucao_filha[vertice] = contador_cores
                  solucao_mae1_limpa[vertice] = -1
                  solucao_mae2_limpa[vertice] = -1
                  contador_vertices_pintados = contador_vertices_pintados + 1
            else:
              primeira_mae = random.randint(1,2)
              flag_mae = primeira_mae                
              if flag_mae == 1:
                flag_mae = 2
                for vertice in range(vertices):
                  if (solucao_mae1[vertice] == cor_maior_mae1) and (solucao_mae2_limpa[vertice] != -1): 
                    solucao_filha[vertice] = contador_cores
                    solucao_mae1_limpa[vertice] = -1
                    solucao_mae2_limpa[vertice] = -1
                    contador_vertices_pintados = contador_vertices_pintados + 1
              elif flag_mae == 2:
                flag_mae = 1
                for vertice in range(vertices):
                  if (solucao_mae2[vertice] == cor_maior_mae2) and (solucao_mae1_limpa[vertice] != -1):
                    solucao_filha[vertice] = contador_cores
                    solucao_mae1_limpa[vertice] = -1
                    solucao_mae2_limpa[vertice] = -1
                    contador_vertices_pintados = contador_vertices_pintados + 1
            contador_cores = contador_cores + 1
          return indice_mae1, indice_mae2, solucao_filha
    
        def melhorar_sol_inicial(grafo, sol_inicial_filha):
          """
          Função que usa o algoritmo tabucol para melhorar a solução filha gerada na iteração
          """
          tabucol = Metaheuristicas().tabucol
          try:
            grafo_c_solucao = tabucol(grafo, sol_inicial_filha, msg_print=False)
            return grafo_c_solucao.vs["cor"]
          except:
            return sol_inicial_filha
        
        def colisoes(grafo, solucao):
          """
          Função simples para cálculo de colisoes
          """
          colisoes = 0
          lista_arestas = grafo.get_edgelist()
          for v_1, v_2 in lista_arestas:
            if solucao[v_1]==solucao[v_2]:
              colisoes = colisoes + 1
          return colisoes 

        def substitui_mae(populacao, indice_mae1, indice_mae2):
          """
          Função usada para determinar qual mãe será substituida na iteração
          """
          colisoes_mae1 = colisoes(grafo, populacao[indice_mae1])
          colisoes_mae2 = colisoes(grafo, populacao[indice_mae2])
          if colisoes_mae1 > colisoes_mae2:
            return indice_mae1
          elif colisoes_mae1 > colisoes_mae2:
            return indice_mae2
          else:
            indices = [indice_mae1, indice_mae2]
            return random.choice(indices)
        
        def sol_final(grafo, populacao):
          """
          Função que retorna a solução que vai ser devolvida pelo algoritmo após as iterações.
          """
          lista_colisoes = []
          for solucao in populacao:
            lista_colisoes.append(colisoes(grafo, solucao)) 
          menos_colisoes = min(lista_colisoes)
          indices_menos_colisoes = []
          for indice, n_colisoes in enumerate(lista_colisoes):
                if n_colisoes == menos_colisoes:
                    indices_menos_colisoes.append(indice)
          indice_escolhido = random.choice(indices_menos_colisoes)
          return populacao[indice_escolhido]
    
        pop_solucoes = criar_pop_inicial(grafo, n_pop)

        iteracoes = 0

        while(iteracoes < iteracoes_tuning):
          iteracoes = iteracoes + 1
          indice_mae1, indice_mae2, sol_filha = operador_recombinacao(pop_solucoes, n_pop, grafo.vcount())
          sol_filha_melhorada = melhorar_sol_inicial(grafo, sol_filha)
          mae_substituida = substitui_mae(pop_solucoes, indice_mae1, indice_mae2)
          pop_solucoes[mae_substituida] = sol_filha_melhorada
        
        sol_final = sol_final(grafo, pop_solucoes)
            
        grafo.vs["cor"] = sol_final
        
        return grafo
 
    def colonia_formigas(grafo, n_formigas = 20, max_iteracoes = 20, alfa = 1, beta = 1, evaporacao = 0.75):

        def peso_trilha_global(vertice, cor):
            """
            Função responsável por calcular o peso da influência da trilha global
            na decisão de adicionar ou não um vértice à coloração
            """
            sum_trilha_global = 0
            for vertice_colorido in cor:
                sum_trilha_global = sum_trilha_global + matriz_global[vertice][vertice_colorido]
            influencia_trilha_global = sum_trilha_global / len(cor)
            return influencia_trilha_global
        
        def peso_heuristica(grafo, vertice, n_coloridos):
            """
            Função que calcula o valor de uma heurística responsável por favorecer a adição
            do vértice à cor. Aqui a heurística considerada é o grau do vértice escolhido no
            grafo induzido pelos vértices ainda não coloridos
            """
            grafo_induzido = grafo.induced_subgraph(vertices=n_coloridos, implementation="create_from_scratch")
            novo_vertice = n_coloridos.index(vertice)
            grau_vertice = grafo_induzido.degree(novo_vertice)
            return grau_vertice

        def peso_individual_vertice(grafo, vertice, cor, n_coloridos):
            """
            Considerando as contribuições da trilha global e da heurística calculamos
            um peso final multiplicando essas duas últimas
            """
            peso_trilha = peso_trilha_global(vertice, cor)
            peso_grau = peso_heuristica(grafo, vertice, n_coloridos)
            peso_vertice = peso_trilha * peso_grau
            return peso_vertice

        def peso_n_coloridos(grafo, cor, n_coloridos):
            """
            Temos que considerar a soma dos pesos de todos os vértices ainda não coloridos,
            isso é, calcular e somar os pesos individuais de cada vértice ainda não colorido 
            segundo nossa função de probabilidade
            """
            sum_pesos = sum(peso_individual_vertice(grafo, vertice, cor, n_coloridos) for vertice in n_coloridos)
            return sum_pesos

        def probabilidade_inclusao(grafo, cor, vertice, n_coloridos, alfa, beta):
            """
            Função responsável por juntar todas as funções peso definidas e devolver um
            número entre 0 e 1 que indica a probabilidade do vértice ser adicionado ou não a cor
            """
            peso_vertice = (peso_trilha_global(vertice, cor)**alfa) * (peso_heuristica(grafo, vertice, n_coloridos)**beta)
            peso_outros = peso_n_coloridos(grafo, cor, n_coloridos)
            if peso_outros == 0:
                return 1
            return peso_vertice/peso_outros

        def coloracao_vertices(grafo, vertice_escolhido, cores, vertices_n_coloridos, vertices_n_coloridos_aux):
            """
            Para cada vértice colorido é necessário que sejam seguidas algumas etapas
            de atualização das estruturas de dados mantidas pelo algoritmo. Essa função faz
            essas atualizações e devolve para o RLF personalizado que é usado aqui no
            Colônia de Formigas
            """
            cores[-1].add(vertice_escolhido)
            vertices_n_coloridos.remove(vertice_escolhido)
            grafo.vs[vertice_escolhido]['cor'] = cores.index(cores[-1])
            vertices_n_coloridos_aux.remove(vertice_escolhido)
            vizinhos_vertice_colorido = grafo.neighbors(vertice_escolhido)
            vertices_n_coloridos_aux = [v for v in vertices_n_coloridos_aux if v not in vizinhos_vertice_colorido]
            return grafo, cores, vertices_n_coloridos, vertices_n_coloridos_aux

        def rlf_colonia_formigas(grafo, n_vertices, cores_max):
            """
            Para construir as soluções de cada "formiga" o colônia de formigas usa uma adaptação do RLF
            já implementado na classe de heurísticas, porém, com algumas adaptações. As adaptações são:
            1 - Um número máximo de cores é permitido durante a construção da solução; 2 - A escolha do
            primeiro vértice de cada cor nova é aleatória; 3 - Os vértices não coloridos até o esgotamento
            do número máximo de cores permanecem não coloridos.
            """
            vertices_n_coloridos = list(range(n_vertices))
            cores_usadas = 0
            grafo.vs['cor'] = [-1] * n_vertices
            cores = []
            while len(vertices_n_coloridos) != 0 and cores_usadas < cores_max:
                cores.append(set())
                vertices_n_coloridos_aux = vertices_n_coloridos.copy()
                while len(vertices_n_coloridos_aux) != 0:
                    vertice_escolhido = random.choice(vertices_n_coloridos_aux)
                    if len(cores[-1]) == 0:
                      grafo, cores, vertices_n_coloridos, vertices_n_coloridos_aux = coloracao_vertices(grafo, vertice_escolhido, cores, vertices_n_coloridos, vertices_n_coloridos_aux)
                    else:
                      probabilidade = probabilidade_inclusao(grafo, cores[-1], vertice_escolhido, vertices_n_coloridos_aux, alfa, beta)
                      adicionado = np.random.binomial(1, probabilidade)
                      if adicionado == 1:
                        grafo, cores, vertices_n_coloridos, vertices_n_coloridos_aux = coloracao_vertices(grafo, vertice_escolhido, cores, vertices_n_coloridos, vertices_n_coloridos_aux)
                      else:
                        vertices_n_coloridos_aux.remove(vertice_escolhido)
                cores_usadas = cores_usadas + 1
            return grafo
        
        def melhorar_sol_inicial(grafo, sol_inicial):
            """
            Caso a solução inicialmente construída com o RLF seja incompleta, os vértices
            não coloridos são atribuidos aleatoriamente. Para melhorar essa situação usamos
            o tabucol com a solução já construída.
            """
            tabucol = Metaheuristicas().tabucol
            try:
                grafo_c_solucao = tabucol(grafo, sol_inicial, msg_print=False)
                return grafo_c_solucao.vs["cor"]
            except:
                return sol_inicial
        
        def solucao_valida(grafo):
            """
            Função que itera sobre o grafo e verifica se a coloração atruibuida a ele é válida ou não.
            """
            lista_adj = grafo.get_adjlist()
            for vertice in range(grafo.vcount()):
                for vizinho in lista_adj[vertice]:
                    if grafo.vs[vertice]["cor"] == grafo.vs[vizinho]["cor"]:
                        return False
            return True
        
        def feromonio(grafo, n_vertices, matriz_local):
            """
            Função que aplica o conceito de fermônio na matriz local da iteração específica.
            O feromônio tratado no algoritmo nada mais é que uma função que aumenta o valor da
            matriz local quando dois vértices estão na mesma cor em uma determinada solução viável.
            """
            for vertice1 in range(n_vertices):
                for vertice2 in range(n_vertices):
                    if vertice1 != vertice2:
                        if grafo.vs['cor'] == grafo.vs['cor']:
                            matriz_local[vertice1][vertice2] = matriz_local[vertice1][vertice2] + 3
                        else:
                            matriz_local[vertice1][vertice2] = matriz_local[vertice1][vertice2] + 0.5
            return matriz_local

        n_vertices = grafo.vcount()
        matriz_global = np.zeros((n_vertices, n_vertices))
        cores_max = n_vertices
        melhor_solucao = igraph.Graph()

        for iteracao in range(max_iteracoes):
            matriz_local = np.zeros((n_vertices, n_vertices))
            min_cores = cores_max
            encontrou_viavel = False
            for formiga in range(n_formigas):
                solucao = rlf_colonia_formigas(grafo, n_vertices = n_vertices, cores_max = n_vertices)
                if (-1) in solucao.vs['cor']:
                    solucao.vs['cor'] = [cor if cor != (-1) else random.choice(range(max(solucao.vs['cor'])+1)) for cor in solucao.vs['cor']]
                    grafo = melhorar_sol_inicial(solucao, solucao.vs['cor'])
                if solucao_valida(grafo) is True:
                    encontrou_viavel = True
                    if len(set(solucao.vs['cor'])) < min_cores:
                        melhor_solucao = grafo
                matriz_local = matriz_local + feromonio(grafo, n_vertices, matriz_local)
            matriz_global = (matriz_global * evaporacao) + matriz_local
            if encontrou_viavel == True:
                min_cores = min_cores - 1
        
        return melhor_solucao



