FLAGSDIR=flags

# core
CORE_PATH=core
CORE_PROJECT=$(FLAGSDIR)/$(CORE_PATH)

JINJA2_PATH=jinja2
JINJA2_PROJECT=$(FLAGSDIR)/$(JINJA2_PATH)

EXAMPLE_PATH=example
EXAMPLE_PROJECT=$(FLAGSDIR)/$(EXAMPLE_PATH)

PROJECTS=$(CORE_PROJECT) $(JINJA2_PROJECT) $(EXAMPLE_PROJECT)

# virtualenv
VIRUALENV=venv_impaf
ACTIVATE=source $(VIRUALENV)/bin/activate

all: $(PROJECTS)

$(CORE_PROJECT): $(CORE_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(CORE_PATH) && python setup.py develop
	@touch $(CORE_PROJECT)

$(JINJA2_PROJECT): $(JINJA2_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(JINJA2_PATH) && python setup.py develop
	@touch $(JINJA2_PROJECT)

$(EXAMPLE_PROJECT): $(EXAMPLE_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(EXAMPLE_PATH) && python setup.py develop
	@touch $(EXAMPLE_PROJECT)

venv_impaf:
	virtualenv $@
	mkdir $(FLAGSDIR)
