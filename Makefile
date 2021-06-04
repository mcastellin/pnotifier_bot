VENV := .venv
PYTHON := $(VENV)/bin/python3

PHONY := all
all:

PHONY += run
run:
	@$(PYTHON) -u main.py
PHONY += fmt
fmt:
	@$(PYTHON) -m black *.py db/*.py services/*.py

.PHONY: $(PHONY)