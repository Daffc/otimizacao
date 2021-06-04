import sys
import pprint
import argparse

def verificaTransformacao(palavra): 
  try:
    return int(palavra)
  except ValueError:
    exit(f'"{palavra}" não é um inteiro válido')

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

def gerarMatrizPadroes(tmp_total, tempos, menor_tempo):

  # Inicializa todas as 'bolsas' com valor de moeda.
  bolsas = [[coin] for coin in tempos]
  new_bolsas = []
  matriz_padrões = []

  # Enquanto existires 'bolsas' passíveis de incremento.
  while bolsas:

    for bolsa in bolsas:
      soma = sum(bolsa)
      reminder = tmp_total - soma
      
      # Caso 'bolsa[0]' já preencha o máximo possível.
      if ((reminder < menor_tempo) and (reminder >= 0)):
        matriz_padrões.append([0]*len(tempos))
        for coin in (bolsa):
          matriz_padrões[-1][tempos.index(coin)] += 1
        next
      
      # Pra cada 'coin' in 'tempos':
      for coin in tempos:

        # Caso nova 'coin' seja maior que a anteriormente adicionada:
        if coin >= bolsa[-1]:
          reminder = tmp_total - (soma + coin)
          
          # Caso seja possível adicionar 'coin', adiciona 'coin' em 'bolsa' cria nova 'bolsa' em 'new_bolsa' 
          if (reminder >=  menor_tempo):
            new_bolsas.append(bolsa + [coin])
            
          # Caso não seja possível adicionar 'coin', maximal encontrado, registrar em matriz.
          elif ((reminder < menor_tempo) and (reminder >= 0)):   

            matriz_padrões.append([0]*len(tempos))
            for coin in (bolsa + [coin]):
              matriz_padrões[-1][tempos.index(coin)] += 1

    # define 'bolsas' com lista de 'bolsa' que ainda são passíveis de incremento ('new_bolsas')
    bolsas = new_bolsas
    new_bolsas = []
  
  return matriz_padrões

def imprimeFormatoLp_solve (problema):

  variaveis_padrao = [  f'x{order}' for order, _ in enumerate(problema['matriz_padroes'])]

  funcao_objeto = 'min: ' + (' + '.join(str(e) for e in variaveis_padrao))

  print(funcao_objeto,';','\n')
  
  for idx, pedido in enumerate(problema['pedidos']):
    for var, linha in zip(variaveis_padrao, problema['matriz_padroes']):
      if(linha[idx] > 0) :
        print( '+', linha[idx],var , end=' ')
    print( ' >= ', pedido[0], ';')

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