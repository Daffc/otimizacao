import sys

TEMPO_MAXIMO = 540

def constroiEstruturas(tempo_total):
    problema = {}
    
    #Definindo Tempo Total
    problema["tempo_total"] = tempo_total
    
    #Lendo Entradas
    lines = [line.strip() for line in sys.stdin.readlines()]
    line_words = lines[0].split()

    problema['qtn_maquinas'] = int(line_words[0])
    problema['qtn_tempos'] = int(line_words[1])

    problema['pedidos'] = []
    for index,line in enumerate(lines[1:]):
        if (index >= problema['qtn_tempos']):
            exit(f'Existem mais tempos do que o especificado. (Maximo: {problema["qtn_tempos"]})')
            
        line_words = line.split()
        problema['pedidos'].append((int(line_words[0]), int(line_words[1])))

    return problema

def main():
    
    # Armazenando Valores de Entrada do problema
    problema = constroiEstruturas(TEMPO_MAXIMO)
    print(problema)



if __name__ == "__main__":
    main()