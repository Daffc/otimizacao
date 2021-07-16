# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pprint import pprint
from problema import Problema, constroiProblema
import bisect

# Busca em profundidade sem Bounds.
def buscaProdundidade(problema, v, total, caminho):

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

  # Percorrer lista de vertices válidos.
  for w in problema.verticesValidos:
    
    peso_aresta = problema.matAdj[v][w]
    # Caso exista aresta '{v, w}'.
    if(peso_aresta>0):
      # Caso não seja possível, passar para próximo vertice.
      buscaProdundidade(problema, w, total + peso_aresta, caminho)

  # Libera visitas à vertice 'v'.
  bisect.insort(problema.verticesValidos,v)

  # Remove 'v' de caminho.
  caminho.pop()

def encontraMaiorCaminhada(problema):

  problema.tempo = datetime.now()
  problema.nosArvore = 1

  # Percorrer linha da matriz correspondente a vertice inicial ('0')
  for w, peso_aresta in enumerate(problema.matAdj[0]):
    if(peso_aresta>0):
      problema.removeAresta(0, w)
      buscaProdundidade(problema, w, peso_aresta, [0])
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
  encontraMaiorCaminhada(problema)
  

if __name__ == "__main__":
  main()
