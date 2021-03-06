# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from problema import Problema, constroiProblema
import bisect

#Percorre matriz de adjacência, somando valor para arestas cujos vetores ainda não foram visitados(cor = 1)
def boundSomaArestas(problema, total):
  soma = total

  # Para todos vertices válidos, exceto origem de caminho.
  for v in problema.verticesValidos[1:]:
    maximo = 0

    # Percorre novamente a lista de vertices válidos com origem incluso.
    for w in problema.verticesValidos:
      # Verifica se contem aresta (peso_aresta > 0) e se é maior aresta encontrada saindo vertice 'v'
      peso_aresta = problema.matAdj[v][w]
      if(peso_aresta  > maximo):
        maximo = peso_aresta
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

  # Remove 'v' de vertices válidos (verticesValidos), garantindo ciclo simples.
  problema.verticesValidos.remove(v)

  bound = boundSomaArestas(problema, total) 

  # Percorrer lista de vertices válidos.
  for w in problema.verticesValidos:
    
    peso_aresta = problema.matAdj[v][w]
    # Caso exista aresta '{v, w}'.
    if(peso_aresta>0):
      # Considerando a adição da aresta 'v -> w', estima se é possível obter uma melhor resposta que a atual.
      if( bound + peso_aresta > problema.tamanhoCicloMax):    
        # Caso não seja possível, passar para próximo vertice.
        buscaProdundidadeBB(problema, w, total + peso_aresta, caminho)

  # Libera visitas à vertice 'v'.
  bisect.insort(problema.verticesValidos,v)

  # Remove 'v' de caminho.
  caminho.pop()

def encontraMaiorCaminhadaBB(problema):

  problema.tempo = datetime.now()
  problema.nosArvore = 1

  bound = boundSomaArestas(problema, 0)

  # Percorrer linha da matriz correspondente a vertice inicial ('0')
  for w, peso_aresta in enumerate(problema.matAdj[0]):
    if(peso_aresta>0):

      # Considerando a adição da aresta '0 -> w', estima se é possível obter um melhor resposta que a atual.
      if(bound + peso_aresta > problema.tamanhoCicloMax):    
        # Caso seja possível, remover aresta e iniciar busca em prodfundidade.
        problema.removeAresta(0, w)
        buscaProdundidadeBB(problema, w, peso_aresta, [0])
        problema.adicionaAresta(0, w, peso_aresta)

  # Marcando tempo e salvando intervalo.
  problema.tempo = datetime.now() - problema.tempo

  # Imprimindo resposta
  print(problema.tamanhoCicloMax)
  print (' '.join([str(x+1) for x in problema.maiorCicloSimples]))
  print >> sys.stderr, "nos_arvore:", problema.nosArvore, "\ntempo:", problema.tempo.total_seconds()

def main():

  #Inicializando Problema
  problema = Problema()

  #Recupera informações de problema de entrada padrão e retorna em objeto 'problema'.
  constroiProblema(problema)

  # Resolve Problema !!!
  encontraMaiorCaminhadaBB(problema)
  

if __name__ == "__main__":
  main()
