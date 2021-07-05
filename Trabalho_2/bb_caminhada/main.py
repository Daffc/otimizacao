#TODO: Remover linhas com "# PRINTDEBUG"


import sys
from datetime import datetime
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

  # Bloqueia visitas à 'vertice' (cores[vertice] = 0), garantindo ciclo simples.
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
  resolverProblema(problema)
  

if __name__ == "__main__":
  main()
