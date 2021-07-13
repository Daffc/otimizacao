# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pprint import pprint
from problema import Problema, constroiProblema
import bisect

#Percorre matriz de adjacência, somando valor para arestas cujos vetores ainda não foram visitados(cor = 1)
def boundSomaArestas(problema, total):
  soma = total

  # Para todos vertices válidos, exceto origem de caminho.
  for v in problema.vert_validos[1:]:
    maximo = 0

    # Percorre novamente a lista de vertices válidos com origem incluso.
    for w in problema.vert_validos:
      # Verifica se contem aresta (peso > 0) e se é maior aresta encontrada saindo vertice 'v'
      peso = problema.grafo[v][w]
      if(peso  > maximo):
        maximo = peso
    soma += maximo
  return soma 


# Busca em profundidade sem Bounds.
def buscaProdundidadeBB(problema, v, total, caminho):

  # Adiciona 'vertice' a caminho.
  caminho.append(v)

  # Caso exita aresta entre vertice atual e vertice 0 (início), uma solução viável foi encontrada.
  if( v == 0 ):

    #Caso solução viável seja maxímal até o momento, armazenar caminho e tamanho.
    if (total > problema.tamanhoCicloMax):

      problema.tamanhoCicloMax = total
      problema.maiorCicloSimples = list(caminho)

    caminho.pop()
    return  

  #Adiciona vertice atual a árvore
  problema.nosArvore += 1

  # Remove 'v' de vertices válidos (vert_validos), garantindo ciclo simples.
  problema.vert_validos.remove(v)

  # Percorrer lista de vertices válidos.
  for w in problema.vert_validos:
    
    peso = problema.grafo[v][w]
    # Caso exista aresta '{v, w}'.
    if(peso>0):
      aux_peso = total + peso
      # Considerando a adição da aresta 'v -> w', estima se é possível obter uma melhor resposta que a atual.
      if(boundSomaArestas(problema, aux_peso)  > problema.tamanhoCicloMax):    
        # Caso não seja possível, passar para próximo vertice.
        buscaProdundidadeBB(problema, w, aux_peso, caminho)

  # Libera visitas à vertice 'v'.
  bisect.insort(problema.vert_validos,v)

  # Remove 'v' de caminho.
  caminho.pop()

def encontraMaiorCaminhadaBB(problema):

  problema.tempobb = datetime.now()
  problema.nosArvore = 1

  # Percorrer linha da matriz correspondente a vertice inicial ('0')
  for w, peso in enumerate(problema.grafo[0]):
    if(peso>0):

      # Considerando a adição da aresta '0 -> w', estima se é possível obter um melhor resposta que a atual.
      if(boundSomaArestas(problema, peso) > problema.tamanhoCicloMax):    
        # Caso seja possível, remover aresta e iniciar busca em prodfundidade.
        problema.removeAresta(0, w)
        buscaProdundidadeBB(problema, w, peso, [0])
        problema.adicionaAresta(0, w, peso)


      
  problema.tempobb = datetime.now() - problema.tempobb

  print( problema.tamanhoCicloMax)
  print >> sys.stderr, ' '.join([str(x+1) for x in problema.maiorCicloSimples])
  print >> sys.stderr, "nos_arvore:", problema.nosArvore, "\ntempo:", problema.tempobb 

def main():

  #Inicializando Problema
  problema = Problema()

  #Recupera informações de problema de entrada padrão e retorna em objeto 'problema'.
  constroiProblema(problema)

  # Resolve Problema !!!
  encontraMaiorCaminhadaBB(problema)
  

if __name__ == "__main__":
  main()
