PYTHON := python2
PIP := pip2

.DEFAULT_GOAL := all
.PHONY := install all clean purge

venv:
	virtualenv -p $(PYTHON) venv

install: venv
	. $</bin/activate && $(PIP) install -r requirements.txt	

caminhada: venv install
	echo "#! /usr/bin/env bash" > caminhada
	echo "source venv/bin/activate" >> caminhada
	echo "pypy bb_caminhada/main.py" $(MAXIMO)  >> caminhada
	echo "deactivate" >> caminhada
	chmod a+x caminhada

all: caminhada

clean:
	-rm caminhada || true

purge: clean
	-rm -rf venv || true
	-rm -rf bb_caminhada/__pycache__
	