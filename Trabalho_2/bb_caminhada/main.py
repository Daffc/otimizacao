import sys
from pprint import pprint

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

  def setVertices(self, vertices):
    if (vertices <= 0):
      exit(f'ERRO: Quatidade de vérices deve ser maior que 0.')

    self.vertices = vertices
    self.grafo = [[0 for col in range(vertices)] for row in range(vertices)]

  def adicionaAresta(self, v_ori, v_dest, valor):
    #Verifica se peso é positivo
    if(valor < 0 ):
      exit(f'ERRO: Distância \'{valor}\' inválida.')
    #Verifica se v_ori é um vértice válido.
    if(v_ori < 0 or v_ori >= self.vertices):
      exit(f'ERRO: Vertice \'{v_ori}\' inválido. (somente de 0 à {self.vertices - 1})')

    #Verifica se v_dest é um vértice válido.
    if(v_dest < 0 or v_dest >= self.vertices):
      exit(f'ERRO: Vertice \'{v_dest}\' inválido. (somente de 0 à {self.vertices - 1})')

    # Adiciona valor a matrix de adjacencia(simétrica).
    self.grafo[v_ori][v_dest] = self.grafo[v_dest][v_ori] = valor
    return 0

  def imprimeProblema(self):
    print(self.vertices)
    pprint(self.grafo)
    
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
      exit(f'ERRO: Quantidade informada de pesos inválida (para vertice \'{v_ori}\' somente \'{v_dest + 1}\' pesos indicados).')

    # Percorre pesos, adicionando-os a valores de aresta.
    for v_dest, palavra in enumerate(palavas_linha):
      destino = v_ori + v_dest + 1
      valor = verificaTransformacao(palavra)
      problema.adicionaAresta(v_ori, destino, valor)

  return problema

def main():
  #Inicializando Problema
  problema = Problema()

  #Recupera informações de problema de entrada padrão e retorna em objeto 'problema'.
  constroiProblema(problema)

  problema.imprimeProblema()

if __name__ == "__main__":
  main()
