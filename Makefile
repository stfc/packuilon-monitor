PYTHON=python2
clean:
	rm -f src/*.pyc test/*.pyc

run:
	$(PYTHON) src/monitor.py

.PHONY: clean run
