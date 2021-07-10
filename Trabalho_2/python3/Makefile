PYTHON := python3
PIP := pip3

MAXIMO ?= 540

.DEFAULT_GOAL := all
.PHONY := install all clean purge

venv:
	virtualenv -p $(PYTHON) venv

install: venv
	. $</bin/activate && $(PIP) install .	

caminhada: venv install
	echo "#! /usr/bin/env bash" > caminhada
	echo "source venv/bin/activate" >> caminhada
	echo "bb-caminhada" $(MAXIMO)  >> caminhada
	echo "deactivate" >> caminhada
	chmod a+x caminhada

all: caminhada

clean:
	-rm caminhada || true

purge: clean
	-rm -rf venv || true