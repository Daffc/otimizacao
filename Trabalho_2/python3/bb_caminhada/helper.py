from pprint import pprint

#  Verifica se valor de 'palavra' pode ser interpretado como interiro. Caso verdadeiro retorna.
def verificaTransformacao(palavra): 
  try:
    return int(palavra)
  except ValueError:
    exit(f'ERRO: "{palavra}" não é um inteiro válido')