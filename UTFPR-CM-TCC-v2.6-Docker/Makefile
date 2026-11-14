# UTFPR-CM TCC v2.6 - platform-neutral build front end.
# On Windows, install GNU Make (or use Start-Here-Windows.cmd instead).
ifeq ($(OS),Windows_NT)
  PYTHON ?= py -3
else
  PYTHON ?= python3
endif
PROJECT ?=
MAIN ?= main.tex
AUTO_APPROVE ?= 0
EXTRA ?=
APPROVE_FLAG = $(if $(filter 1 yes true,$(AUTO_APPROVE)),--yes,)
PROJECT_FLAG = $(if $(PROJECT),--project "$(PROJECT)",)
.PHONY: all compile setup doctor clean help strict refresh-image test
all: compile
compile:
	$(PYTHON) scripts/compile.py compile --main "$(MAIN)" $(PROJECT_FLAG) $(APPROVE_FLAG) $(EXTRA)
setup:
	$(PYTHON) scripts/compile.py setup $(APPROVE_FLAG) $(EXTRA)
doctor:
	$(PYTHON) scripts/compile.py doctor
clean:
	$(PYTHON) scripts/compile.py clean
strict:
	$(PYTHON) scripts/compile.py compile --strict --main "$(MAIN)" $(PROJECT_FLAG) $(APPROVE_FLAG) $(EXTRA)
refresh-image:
	$(PYTHON) scripts/compile.py setup --refresh-image $(APPROVE_FLAG)
help:
	$(PYTHON) scripts/compile.py --help
test:
	$(PYTHON) -m unittest discover -s tests -v
