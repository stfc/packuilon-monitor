PYTHON=python2
PIP=pip
clean:
	rm -f packuilon_monitor/*.pyc test/*.pyc

install:
	sudo $(PIP) install -e .
.PHONY: clean install
