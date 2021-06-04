import sys
import pprint
import argparse

#  Verifica se valor de 'palavra' pode ser interpretado como interiro. Caso verdadeiro retorna.
def verificaTransformacao(palavra): 
  try:
    return int(palavra)
  except ValueError:
    exit(f'"{palavra}" não é um inteiro válido')

# Lê entrada e define estritura para abordar problema.
def constroiEstruturas(tempo_maximo):
  problema = {}
  
  #Definindo Tempo Total
  problema['tempo_maximo'] = tempo_maximo
  
  #Lendo Entradas
  lines = [line.strip() for line in sys.stdin.readlines()]
  line_words = lines[0].split()

  problema['qtn_maquinas'] = verificaTransformacao(line_words[0])
  problema['qtn_tempos'] = verificaTransformacao(line_words[1])

  # Verifica se quantidade de pedidos informada é vádila.
  if (problema['qtn_maquinas'] <= 0):
    exit(f'Quatidade de máquinas deve ser maior que 0.')

  # Verifica se quantidade de pedidos informada é vádila.
  if (problema['qtn_tempos'] <= 0):
    exit(f'Quatidade de tipos de pedido deve ser maior que 0.')

  problema['pedidos'] = []
  for index,line in enumerate(lines[1:]):
    # Verifica se quatidade de tipos de process extrapola o especificado.
    if (index >= problema['qtn_tempos']):
      exit(f'Existem mais tipos de processo que o especificado. (Quantidade Informada: {problema["qtn_tempos"]})')
        
    line_words = line.split()
    qtn_pedido = verificaTransformacao(line_words[0])
    tempo_pedido = verificaTransformacao(line_words[1])

    # Verifica se pedido possui tempo válido
    if(not (0 <=tempo_pedido <= problema['tempo_maximo'])): 
      exit(f'Tempo "{tempo_pedido}" não é válido.')

    # Adiciona tupla (quantidade, valor) a lista 'pedidos'.
    problema['pedidos'].append((qtn_pedido, tempo_pedido))

  if (len(problema['pedidos']) < problema['qtn_tempos']):
    exit(f'Quantidade de tempos recebida inferior a indicada (ENCONTRADOS: {len(problema["pedidos"])}, INDICADO: {problema["qtn_tempos"]})')

  return problema

# Gera Matriz de padrões para problema, contendo padrão em linhas e valores de variáveis em conlunas.
def gerarMatrizPadroes(tmp_total, tempos, menor_tempo):

  # Inicializa todas as 'bolsas' com valor de tempos.
  bolsas = [[tempo] for tempo in tempos]
  matriz_padroes = []

  #  Percorre todas as bolsas verificando se alguma delas já tem valor maximal
  for bolsa in list(bolsas):
    reminder = tmp_total - sum(bolsa)

    # Caso bolsa maximal tenha sido encontrada, inserir seu padrão em 'matriz_padroes' e remover de bolsas.
    if ((reminder < menor_tempo) and (reminder >= 0)):
      matriz_padroes.append([0]*len(tempos))
      matriz_padroes[-1][tempos.index(bolsa[0])] += 1
      bolsas.remove(bolsa)

  new_bolsas = []
  # Enquanto existirem 'bolsas' passíveis de incremento.
  while bolsas:
    for bolsa in bolsas:
      soma = sum(bolsa)

      # Pra cada 'tempo' in 'tempos':
      for tempo in tempos:

        # Caso nova 'tempo' seja maior que a anteriormente adicionada:
        if tempo >= bolsa[-1]:

          reminder = tmp_total - (soma + tempo)

          # Caso seja possível adicionar 'tempo', adiciona 'tempo' em 'bolsa' cria nova 'bolsa' em 'new_bolsa' 
          if (reminder >=  menor_tempo):
            new_bolsas.append(bolsa + [tempo])
            
          # Caso não seja possível adicionar 'tempo', novo maximal encontrado, registrar em matriz_padroes.
          elif ((reminder < menor_tempo) and (reminder >= 0)):   
            # Adiciona novo padrão a matriz_padroes, somando 1 a index de cada 'tempo' em 'bolsa'.
            matriz_padroes.append([0]*len(tempos))
            for tempo in (bolsa + [tempo]):
              matriz_padroes[-1][tempos.index(tempo)] += 1

    # Define 'bolsas' com lista de 'bolsa' que ainda são passíveis de incremento ('new_bolsas')
    bolsas = new_bolsas
    new_bolsas = []
  
  return matriz_padroes

# A partir de dados em 'problema', imprime saida compativel com programa 'lp_solve'
def imprimeFormatoLp_solve (problema):

  # Definindo e printando função objetivo (uma variável para cada padrão encontrado.)
  variaveis_padrao = [  f'x{order}' for order, _ in enumerate(problema['matriz_padroes'])]
  funcao_objeto = 'min: ' + (' + '.join(str(e) for e in variaveis_padrao))
  print(funcao_objeto,';\n')
  
  # Iterando sobre 'pedidos'
  for idx, pedido in enumerate(problema['pedidos']):
    var_restricoes = []
    # Agregando os padrões em que 'pedido' aparece o fator em que aparece; Definindo String que compões lado esquerdo de restrição.
    for var, linha in zip(variaveis_padrao, problema['matriz_padroes']):
      if(linha[idx] > 0) :
        var_restricoes.append(f'{linha[idx]} {var}') 
    # Imprimindo inequação, constando variáveis e valor solicitado de 'pedido'
    print(*var_restricoes, sep = " + ", end='')
    print(' >= ', pedido[0], ';')

# Parsing program initialization arguments. 
def parsingArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("ValorMaximo", help="Indica o valor máximo de minutos por dia-máquina./t")
    args = parser.parse_args()

    return int(args.ValorMaximo)

def main():

  # Recupera tempo máximo de parâmetro de entrada.
  tempo_maximo = parsingArguments()
    
  # Armazenando Valores de Entrada do problema
  problema = constroiEstruturas(tempo_maximo)

  lista_tempos = [tempo[1] for tempo in problema['pedidos']] 
  
  # Gerando matriz de Parões
  problema['matriz_padroes'] = gerarMatrizPadroes(problema['tempo_maximo'], lista_tempos, min(lista_tempos))
  
  # pprint.pprint(problema)
  imprimeFormatoLp_solve(problema)

if __name__ == "__main__":
  main()