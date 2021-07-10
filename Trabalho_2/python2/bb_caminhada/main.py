# -*- coding: utf-8 -*-
#TODO: Remover linhas com "# PRINTDEBUG"

import sys
from datetime import datetime
from pprint import pprint
from problema import Problema, constroiProblema
import bisect
  
#----------------------------
#       CLASSICO
#----------------------------

# Busca em profundidade sem Bounds.
def buscaProdundidadeClassica(problema, vertice, total, caminho):
  
  # print( *['-' for x in caminho],  vertice +1) # PRINTDEBUG
  # Adiciona 'vertice' a caminho.
  caminho.append(vertice)
  # print( [*[x+1 for x in caminho]])


  # Caso exita aresta entre vertice atual e vertice 0 (início), uma solução viável foi encontrada.
  if( vertice == 0 ):

    #Caso solução viável seja maxímal até o momento, armazenar caminho e tamanho.
    if (total > problema.tamanhoMaiorCicloSimples):
      # print(f'parcial: {total}', [*[x+1 for x in caminho]]) # PRINTDEBUG

      problema.tamanhoMaiorCicloSimples = total
      problema.maiorCicloISmples = list(caminho)

    caminho.pop()
    return  

  #Adiciona vertice atual a árvore
  problema.nosArvore += 1

  # Bloqueia visitas à 'vertice' (cores[vertice] = 0), garantindo ciclo simples.
  problema.list_cores.remove(vertice)

  lista_atual = list(problema.list_cores)
  # Percorrer linha da matriz correspondente a 'vertice'
  for idx_vizinho in lista_atual:
    
    peso = problema.grafo[vertice][idx_vizinho]
    # Caso exista aresta e vetor não foi visitado.
    if(peso>0):
      total += peso
      buscaProdundidadeClassica(problema, idx_vizinho, total, caminho)
      total -= peso

  # Libera visitas à 'vertice' (cores[vertice] = 1).
  bisect.insort(problema.list_cores,vertice)

  # Remove 'vertice' de caminho.
  caminho.pop()

#----------------------------
#       Branch and Bound
#----------------------------

#Percorre matriz de adjacência, somando valor para arestas cujos vetores ainda não foram visitados(cor = 1)
def boundSomaArestasValidas(problema, total):
  soma = total

  cores_idx = list(problema.list_cores)

  for idx in cores_idx[1:]:
    maximo = 0
    for idx_col in cores_idx:
      peso = problema.grafo[idx][idx_col]
      if(peso  > maximo):
        maximo = peso
    # print("maximo", idx, maximo)
    soma += maximo
    

  # print(total, soma, problema.tamanhoMaiorCicloSimples) # PRINTDEBUG
  # print("***", total, soma) # PRINTDEBUG
  return soma 


# Busca em profundidade sem Bounds.
def buscaProdundidadeBB(problema, vertice, total, caminho):

  # print( *['-' for x in caminho],  vertice +1) # PRINTDEBUG
  # Adiciona 'vertice' a caminho.
  caminho.append(vertice)
  # print( [*[x+1 for x in caminho]])


  # Caso exita aresta entre vertice atual e vertice 0 (início), uma solução viável foi encontrada.
  if( vertice == 0 ):

    #Caso solução viável seja maxímal até o momento, armazenar caminho e tamanho.
    if (total > problema.tamanhoMaiorCicloSimples):
      # print(f'parcial: {total}', [*[x+1 for x in caminho]]) # PRINTDEBUG

      problema.tamanhoMaiorCicloSimples = total
      problema.maiorCicloISmples = list(caminho)

    caminho.pop()
    return  

  #Adiciona vertice atual a árvore
  problema.nosArvore += 1

  # Bloqueia visitas à 'vertice' (cores[vertice] = 0), garantindo ciclo simples.
  problema.list_cores.remove(vertice)

  lista_atual = list(problema.list_cores)
  # Percorrer linha da matriz correspondente a 'vertice'
  for idx_vizinho in lista_atual:
    
    peso = problema.grafo[vertice][idx_vizinho]
    # Caso exista aresta e vetor não foi visitado.
    if(peso>0):

      total += peso

      # Considerando a adição da aresta 'vertice -> idx_vizinho', estima se é possível obter uma melhor resposta que a atual.
      if(boundSomaArestasValidas(problema, total + peso)  <= problema.tamanhoMaiorCicloSimples):    
        # Caso não seja possível, passar para próximo vertice.
        total -= peso
        continue

      buscaProdundidadeBB(problema, idx_vizinho, total, caminho)
      total -= peso

  # Libera visitas à 'vertice' (cores[vertice] = 1).
  bisect.insort(problema.list_cores,vertice)

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
  print >> sys.stderr, ' '.join([str(x+1) for x in problema.maiorCicloISmples])
  print >> sys.stderr, "nos_arvore:", problema.nosArvore, "\ntempo:", problema.tempo

  # problema.imprimeProblema() # PRINTDEBUG
  print("---------------------") # PRINTDEBUG

  #############################
  # Problema Branch and Bound #
  #############################
  problema.tamanhoMaiorCicloSimples = 0
  problema.maiorCicloISmples = []
  # problema.cores = [1] * problema.vertices
  problema.list_cores = [s for s in range(problema.vertices)]

  print("-------- BB --------") # PRINTDEBUG
  # problema.imprimeProblema() # PRINTDEBUG

  problema.tempobb = datetime.now()
  problema.nosArvore = 1

  # Percorrer linha da matriz correspondente a vertice inicial ('0')
  for idx_vizinho, peso in enumerate(problema.grafo[0]):
    if(peso>0):

      problema.removeAresta(0, idx_vizinho)
      
      # Considerando a adição da aresta '0 -> idx_vizinho', estima se é possível obter uma melhor resposta que a atual.
      if(boundSomaArestasValidas(problema, peso)  <= problema.tamanhoMaiorCicloSimples):    
        # Caso não seja possível, passar para próximo vertice.
        continue

      buscaProdundidadeBB(problema, idx_vizinho, peso, [0])
      problema.adicionaAresta(0, idx_vizinho, peso)
      
  problema.tempobb = datetime.now() - problema.tempobb

  print( problema.tamanhoMaiorCicloSimples)
  print >> sys.stderr, ' '.join([str(x+1) for x in problema.maiorCicloISmples])
  print >> sys.stderr, "nos_arvore:", problema.nosArvore, "\ntempo:", problema.tempobb 

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
