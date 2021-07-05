#TODO: Remover linhas com "# PRINTDEBUG"

import sys
from pprint import pprint
from datetime import datetime

#  Verifica se valor de 'palavra' pode ser interpretado como interiro. Caso verdadeiro retorna.
def verificaTransformacao(palavra): 
  try:
    return int(palavra)
  except ValueError:
    exit(f'ERRO: "{palavra}" não é um inteiro válido')

class Problema:

  def __init__(self):
    self.vertices = 0
    self.grafo = []
    self.cores = []
    self.maiorCicloISmples = []
    self.tamanhoMaiorCicloSimples = 0
    self.nosArvore = 0
    self.tempo = 0

  def setVertices(self, vertices):
    if (vertices <= 0):
      exit(f'ERRO: Quatidade de vérices deve ser maior que 0.')

    self.vertices = vertices
    self.grafo = [[0 for col in range(vertices)] for row in range(vertices)]
    self.cores = [1] * vertices

  def verificaEAdicionaAresta(self, v_ori, v_dest, valor):
    #Verifica se peso é positivo
    if(valor < 0 ):
      exit(f'ERRO: Distância \'{valor}\' inválida.')
    #Verifica se v_ori é um vértice válido.
    if(v_ori < 0 or v_ori >= self.vertices):
      exit(f'ERRO: Vertice \'{v_ori}\' inválido. (somente de 0 à {self.vertices - 1})')

    #Verifica se v_dest é um vértice válido.
    if(v_dest < 0 or v_dest >= self.vertices):
      exit(f'ERRO: Vertice \'{v_dest}\' inválido. (somente de 0 à {self.vertices - 1})')
    
    # Efetua adição de aresta
    self.adicionaAresta(v_ori, v_dest, valor)

  # Adiciona Aresta a matriz de adjacência 'grafo'.
  def adicionaAresta(self, v_ori, v_dest, valor):
    # Adiciona valor a matrix de adjacencia(simétrica).
    self.grafo[v_ori][v_dest] = self.grafo[v_dest][v_ori] = valor

  # Remove Aresta a matriz de adjacência 'grafo'.
  def removeAresta(self, v_ori, v_dest):
    # Adiciona valor a matrix de adjacencia(simétrica).
    valor = self.grafo[v_ori][v_dest]
    self.grafo[v_ori][v_dest] = self.grafo[v_dest][v_ori] = 0
    return valor

  # aplica cor a vertice de posição 'vertice' (1 para visitado e 0 para não visitado.)
  def mudarCor(self, vertice, cor):
    self.cores[vertice] = cor

  def imprimeProblema(self):
    print(self.vertices)
    pprint(self.grafo)
    pprint(self.cores)


# Lê entrada e define estruturas de problema.
def constroiProblema(problema):

  #Lendo Entradas
  linhas = [linha.strip() for linha in sys.stdin.readlines()]
  palavas_linha = linhas[0].split()

  #Definindo Número de Vértices.
  problema.setVertices(verificaTransformacao(palavas_linha[0]))

  # Verifica se quantidade de linhas de pesos é igual a quantidade de vertices -1.
  if(len(linhas[1:]) < (problema.vertices - 1)):
    exit(f'ERRO: Quantidade list de pesos informada (\'{len(linhas[1:])}\') inferior a esperada(\'{(problema.vertices - 1)}\').')

  # Percorre todas as linhas de pesos.
  for v_ori, linha in enumerate(linhas[1:]):

    palavas_linha = linha.split()

    # Verifica se quantidade de pesos é compativel a vertice v_ori.
    if(len(palavas_linha) != (problema.vertices - v_ori - 1)):
      exit(f'ERRO: Quantidade informada de pesos inválida (para vertice \'{v_ori}\' somente \'{len(palavas_linha)}\' pesos indicados).')

    # Percorre pesos, adicionando-os a valores de aresta.
    for v_dest, palavra in enumerate(palavas_linha):
      destino = v_ori + v_dest + 1
      valor = verificaTransformacao(palavra)
      problema.verificaEAdicionaAresta(v_ori, destino, valor)

  return problema
  
#----------------------------
#       CLASSICO
#----------------------------

# Busca em profundidade sem Bounds.
def buscaProdundidadeClassica(problema, vertice, total, caminho):
  
  # Adiciona 'vertice' a caminho.
  caminho.append(vertice)
  problema.nosArvore += 1
  
  # Caso exita aresta entre vertice atual e vertice 0 (início), uma solução viável foi encontrada.
  if( vertice == 0 ):
    # print(f"---- {total} ----", *[x+1 for x in caminho]) # PRINTDEBUG

    #Caso solução viável seja maxímal até o momento, armazenar caminho e tamanho.
    if (total > problema.tamanhoMaiorCicloSimples):
      problema.tamanhoMaiorCicloSimples = total
      problema.maiorCicloISmples = caminho.copy()

    caminho.pop()
    return  

  # Bloqueia visitas à 'vertice' (cores[vertice] = 1), garantindo ciclo simples.
  problema.mudarCor(vertice, 0)

  # Percorrer linha da matriz correspondente a 'vertice'
  for idx_vizinho, peso in enumerate(problema.grafo[vertice]):
    # Caso exista aresta e vetor não foi visitado.
    if((peso>0) and problema.cores[idx_vizinho]):

      problema.removeAresta(vertice, idx_vizinho)
      total += peso
      buscaProdundidadeClassica(problema, idx_vizinho, total, caminho)
      total -= peso
      problema.adicionaAresta(vertice, idx_vizinho, peso)

  # Libera visitas à 'vertice' (cores[vertice] = 0).
  problema.mudarCor(vertice, 1)

  # Remove 'vertice' de caminho.
  caminho.pop()

#----------------------------
#       Branch and Bound
#----------------------------

#Percorre matriz de adjacência, somando valor para arestas cujos vetores ainda não foram visitados(cor = 1)
def boundSomaArestasValidas(problema):
  soma = 0
  # pprint(problema.grafo) # PRINTDEBUG
  for idx, linha_adj in enumerate(problema.grafo):
      for peso in linha_adj[idx:]:
        soma += peso * problema.cores[idx]
  
  # print("***", soma) # PRINTDEBUG
  return soma 


# Busca em profundidade sem Bounds.
def buscaProdundidadeBB(problema, vertice, total, caminho):
  # Adiciona 'vertice' a caminho.
  caminho.append(vertice)
  problema.nosArvore += 1
  
  
  # Caso exita aresta entre vertice atual e vertice 0 (início), uma solução viável foi encontrada.
  if( vertice == 0 ):
    # print(f"---- {total} ----", *[x+1 for x in caminho]) # PRINTDEBUG

    #Caso solução viável seja maxímal até o momento, armazenar caminho e tamanho.
    if (total > problema.tamanhoMaiorCicloSimples):
      problema.tamanhoMaiorCicloSimples = total
      problema.maiorCicloISmples = caminho.copy()

    caminho.pop()
    return  

  # Bloqueia visitas à 'vertice' (cores[vertice] = 1), garantindo ciclo simples.
  problema.mudarCor(vertice, 0)

  # Percorrer linha da matriz correspondente a 'vertice'
  for idx_vizinho, peso in enumerate(problema.grafo[vertice]):
    # Caso exista aresta e vetor não foi visitado.
    if((peso>0) and problema.cores[idx_vizinho]):
      
      # Caso caso não seja possível ultrapassar valor atual de caminho máximo, retornar(poda)
      if(boundSomaArestasValidas(problema) < problema.tamanhoMaiorCicloSimples):
        # pprint(problema.grafo) # PRINTDEBUG
        # print('\n') # PRINTDEBUG
        problema.mudarCor(vertice, 0)
        caminho.pop()
        return
      problema.removeAresta(vertice, idx_vizinho)
      total += peso
      buscaProdundidadeBB(problema, idx_vizinho, total, caminho)
      total -= peso
      problema.adicionaAresta(vertice, idx_vizinho, peso)

  # Libera visitas à 'vertice' (cores[vertice] = 0).
  problema.mudarCor(vertice, 1)

  # Remove 'vertice' de caminho.
  caminho.pop()

def resolverProblemaClassico(problema):

  # problema.imprimeProblema() # PRINTDEBUG

  #####################
  # Problema Classico #
  #####################

  print("------ Classico --------") # PRINTDEBUG

  problema.tempo = datetime.now()
  problema.nosArvore = 1

  # Percorrer linha da matriz correspondente a 'vertice'
  for idx_vizinho, peso in enumerate(problema.grafo[0]):
    if(peso>0):
      problema.removeAresta(0, idx_vizinho)      
      buscaProdundidadeClassica(problema, idx_vizinho, peso, [0])
      problema.adicionaAresta(0, idx_vizinho, peso)
      
  problema.tempo = datetime.now() - problema.tempo

  
  print(problema.tamanhoMaiorCicloSimples)
  print(*[x+1 for x in problema.maiorCicloISmples])
  print(f"nos_arvore: {problema.nosArvore}\ntempo: {problema.tempo}", file=sys.stderr)

  print("---------------------") # PRINTDEBUG


  #############################
  # Problema Branch and Bound #
  #############################

  print("-------- BB --------") # PRINTDEBUG

  problema.tempo = datetime.now()
  problema.nosArvore = 1

  # Percorrer linha da matriz correspondente a 'vertice'
  for idx_vizinho, peso in enumerate(problema.grafo[0]):
    if(peso>0):
      problema.removeAresta(0, idx_vizinho)      
      buscaProdundidadeBB(problema, idx_vizinho, peso, [0])
      problema.adicionaAresta(0, idx_vizinho, peso)
      
  problema.tempo = datetime.now() - problema.tempo

  print(problema.tamanhoMaiorCicloSimples)
  print(*[x+1 for x in problema.maiorCicloISmples])
  print(f"nos_arvore: {problema.nosArvore}\ntempo: {problema.tempo}", file=sys.stderr)

  print("---------------------") # PRINTDEBUG

  
def main():
  #Inicializando Problema
  problema = Problema()

  #Recupera informações de problema de entrada padrão e retorna em objeto 'problema'.
  constroiProblema(problema)

  # Resolve Problema !!!
  resolverProblemaClassico(problema)

if __name__ == "__main__":
  main()
