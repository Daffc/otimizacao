
import sys
from helper import verificaTransformacao
from pprint import pprint

#Classe agregando estrutudas do problema e suas funcionalidades.
class Problema:

  def __init__(self):
    self.vertices = 0
    self.grafo = []
    self.cores = []
    self.maiorCicloISmples = []
    self.tamanhoMaiorCicloSimples = 0
    self.nosArvore = 0
    self.tempo = 0

  #Verifica entrada e armazena quantidade de verticesd e problema.
  def setVertices(self, vertices):
    if (vertices <= 0):
      exit(f'ERRO: Quatidade de vérices deve ser maior que 0.')

    self.vertices = vertices
    self.grafo = [[0 for col in range(vertices)] for row in range(vertices)]
    self.cores = [1] * vertices

  #Verifica dados de entrada para arestas e chama "adicionaAresta".
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

  # Imprime estruturas de Problema
  def imprimeProblema(self):
    print(self.vertices)
    pprint(self.grafo)
    print(self.cores)


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