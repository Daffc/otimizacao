# lp_tempo

Gerador de modelo de entrada lp para lp_solve com o objetivo de otimizar a realização de processos em dias-máquina.

O relatório de encontra em `./Relatório.pdf`

## Instalação

Para realizar a instalação do projeto, basta executar o comando `make` no diretório corrente, realizando:
- Criação de ambiente virtual `venv`.
- Ativação de ambiente `venv` e instalação de pacotes necessários a `lp_tempo`.
- Definição de `lp_tempo` como módulo de ambiente virtual `venv`.
- Desativação de ambiente virtual.
- Criação de executável `tempo`, que deverá subir ambiente virtual `venv`, executar `lp_tempo` e desativar ambiente virtual.

O projeto é baseado em `Python 3` sendo algumas funcionalidades exclusivas das versões `>= 3.6`. 

OBS Este projeto foi desenvolvido tendo como padrão instâncias unidimensionais do [Cutting stock problem](https://en.wikipedia.org/wiki/Cutting_stock_problem) com itens primários (rolos primários) de dimensão 540. Caso deseje-se utilizar instâncias de dimensões diferentes, utilizando comando `make MAXIMO=X` com `X` sendo a nova dimensão desejada.

## Uso

Apos a instalação, para efetuar o uso da ferrament a travez do exevutável `tempo`, basta:

`./ tempo < entrada.txt`

ou, ativando o ambiente virtual, pode-se chamar diretamente o módulo `lp_tempo`, como:

`lp_tempo < entrada.txt`

### Formato de entrada

O arquivo de entrada deve conter o seguinter formato:
```
qnt_maquinas qnt_classes
qnt_classe0 tmp_classe0
qnt_classe1 tmp_classe1
...
qnt_classeN tmp_classeN
```

Sendo:
- `qnt_maquinas` A quantidade de máquinas disponíveis.
- `qnt_classes` A quantidade de Classes (cortes) solicitadas.
- `qnt_classeN` Quantidade de solicitações (cortes) da Classe N.
- `tmp_classeN` Quantidade de tempo (tamanho do corte) despedido em Classe N.


