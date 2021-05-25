PYTHON := python3
PIP := pip3

.DEFAULT_GOAL := all
.PHONY := install all clean purge

venv:
	virtualenv -p $(PYTHON) venv

install: venv
	. $</bin/activate && $(PIP) install .	

tempo: venv install
	echo "#! /usr/bin/env bash" > tempo
	echo "source venv/bin/activate" >> tempo
	echo "lp-tempo" >> tempo
	echo "deactivate" >> tempo
	chmod a+x tempo

all: tempo

clean:
	-rm tempo 2&> /dev/null || true

purge: clean
	-rm -rf venv 2&> /dev/null || true