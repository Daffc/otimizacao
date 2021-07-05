#TODO: Remover linhas com "# PRINTDEBUG"


import sys
from datetime import datetime
from pprint import pprint
from problema import Problema, constroiProblema 
  
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
def boundSomaArestasValidas(problema, total):
  soma = total

  # pprint(problema.grafo) # PRINTDEBUG
  # print(problema.cores) # PRINTDEBUG
  for idx, linha_adj in enumerate(problema.grafo):
    maximo = 0
    for peso in linha_adj[idx:]:
      aux = peso * problema.cores[idx]
      if(aux > maximo):
        maximo = aux      
    soma += maximo
    # print("\n")
  # print(total, soma, problema.tamanhoMaiorCicloSimples)
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

  # Bloqueia visitas à 'vertice' (cores[vertice] = 0), garantindo ciclo simples.
  problema.mudarCor(vertice, 0)

  # Percorrer linha da matriz correspondente a 'vertice'
  for idx_vizinho, peso in enumerate(problema.grafo[vertice]):
    # Caso exista aresta e vetor não foi visitado.
    if((peso>0) and problema.cores[idx_vizinho]):
      

      problema.removeAresta(vertice, idx_vizinho)
      total += peso
      # Caso caso não seja possível ultrapassar valor atual de caminho máximo, retornar(poda)
      if(boundSomaArestasValidas(problema, total) <= problema.tamanhoMaiorCicloSimples):
        # pprint(problema.grafo) # PRINTDEBUG
        # print('\n') # PRINTDEBUG
        # print("caminho:", caminho) # PRINTDEBUG
        problema.mudarCor(vertice, 1)
        total -= peso
        problema.adicionaAresta(vertice, idx_vizinho, peso)
        caminho.pop()
        return
      buscaProdundidadeBB(problema, idx_vizinho, total, caminho)
      total -= peso
      problema.adicionaAresta(vertice, idx_vizinho, peso)

  # Libera visitas à 'vertice' (cores[vertice] = 1).
  problema.mudarCor(vertice, 1)

  # Remove 'vertice' de caminho.
  caminho.pop()

def resolverProblema(problema):

  # problema.imprimeProblema() # PRINTDEBUG

  #####################
  # Problema Classico #
  #####################

  print("------ Classico --------") # PRINTDEBUG
  # problema.imprimeProblema() # PRINTDEBUG


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

  # problema.imprimeProblema() # PRINTDEBUG
  print("---------------------") # PRINTDEBUG


  #############################
  # Problema Branch and Bound #
  #############################
  problema.tamanhoMaiorCicloSimples = 0
  problema.maiorCicloISmples = []
  problema.cores = [1] * problema.vertices

  print("-------- BB --------") # PRINTDEBUG
  # problema.imprimeProblema() # PRINTDEBUG

  problema.tempobb = datetime.now()
  problema.nosArvore = 1

  # Percorrer linha da matriz correspondente a vertice inicial ('0')
  for idx_vizinho, peso in enumerate(problema.grafo[0]):
    if(peso>0):
      #Verifica se ainda é possível otimizar o resultado de acordo com o bound.
      if(boundSomaArestasValidas(problema, 0) <= problema.tamanhoMaiorCicloSimples):
        continue

      problema.removeAresta(0, idx_vizinho)
      buscaProdundidadeBB(problema, idx_vizinho, peso, [0])
      problema.adicionaAresta(0, idx_vizinho, peso)
      
  problema.tempobb = datetime.now() - problema.tempobb

  print(problema.tamanhoMaiorCicloSimples)
  print(*[x+1 for x in problema.maiorCicloISmples])
  print(f"nos_arvore: {problema.nosArvore}\ntempo: {problema.tempobb}", file=sys.stderr)

  # problema.imprimeProblema() # PRINTDEBUG
  print("---------------------") # PRINTDEBUG  

def main():
  #Inicializando Problema
  problema = Problema()

  #Recupera informações de problema de entrada padrão e retorna em objeto 'problema'.
  constroiProblema(problema)

  # Resolve Problema !!!
  resolverProblema(problema)
  

if __name__ == "__main__":
  main()
