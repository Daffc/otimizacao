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

      total += peso
      buscaProdundidadeClassica(problema, idx_vizinho, total, caminho)
      total -= peso

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

  cores_aux = problema.cores.copy()

  # pprint(problema.grafo) # PRINTDEBUG
  # for l in problema.grafo:  # PRINTDEBUG
  #   print(l)                # PRINTDEBUG

  # print("Cores2:", cores_aux) # PRINTDEBUG

  for idx_lin, linha_adj in enumerate(problema.grafo):
    maximo = 0
    if(cores_aux[idx_lin]):
      cores_aux[idx_lin] = 0
      for idx_col, peso in enumerate(linha_adj):
        if((peso * cores_aux[idx_col]) > maximo):
          maximo = peso
                
    soma += maximo

  # print(total, soma, problema.tamanhoMaiorCicloSimples) # PRINTDEBUG
  # print("***", soma) # PRINTDEBUG
  return soma 


# Busca em profundidade sem Bounds.
def buscaProdundidadeBB(problema, vertice, total, caminho):


  # print( *['  ' for x in caminho],  vertice +1) # PRINTDEBUG

  # Adiciona 'vertice' a caminho.
  caminho.append(vertice)

  # Caso exita aresta entre vertice atual e vertice 0 (início), uma solução viável foi encontrada.
  if( vertice == 0 ):
    # print(f"---- {total} ----", *[x+1 for x in caminho]) # PRINTDEBUG

    #Caso solução viável seja maxímal até o momento, armazenar caminho e tamanho.
    if (total > problema.tamanhoMaiorCicloSimples):
      problema.tamanhoMaiorCicloSimples = total
      problema.maiorCicloISmples = caminho.copy()

    caminho.pop()
    return  

  #Adiciona vertice atual a árvore
  problema.nosArvore += 1

  # Caso caso não seja possível ultrapassar valor atual de caminho máximo, retornar(poda)
  if(boundSomaArestasValidas(problema, total) <= problema.tamanhoMaiorCicloSimples):
    # print("saindo:", vertice +1)
    problema.mudarCor(vertice, 1)
    caminho.pop()
    return

  # Bloqueia visitas à 'vertice' (cores[vertice] = 0), garantindo ciclo simples.
  problema.mudarCor(vertice, 0)

  # Percorrer linha da matriz correspondente a 'vertice'
  for idx_vizinho, peso in enumerate(problema.grafo[vertice]):
    # Caso exista aresta e vetor não foi visitado.
    if((peso>0) and problema.cores[idx_vizinho]):
      total += peso
      buscaProdundidadeBB(problema, idx_vizinho, total, caminho)
      total -= peso

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

      problema.removeAresta(0, idx_vizinho)
      buscaProdundidadeBB(problema, idx_vizinho, peso, [0])
      problema.adicionaAresta(0, idx_vizinho, peso)
      
  problema.tempobb = datetime.now() - problema.tempobb

  print( problema.tamanhoMaiorCicloSimples)
  print( *[x+1 for x in problema.maiorCicloISmples])
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
