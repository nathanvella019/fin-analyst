PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.PHONY: ci lint test validate gate

# Sequential commands also preserve stop-on-failure when make is invoked with -j.
ci:
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) validate
	$(MAKE) gate

lint:
	$(PYTHON) -m ruff check --select E4,E9,F src tests scripts

test:
	$(PYTHON) -m unittest discover -s tests -v

validate:
	$(PYTHON) -m sec_analyst.ci validate

gate:
	$(PYTHON) -m sec_analyst.ci gate
