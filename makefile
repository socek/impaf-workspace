FLAGSDIR=flags

# core
CORE_PATH=core
CORE_PROJECT=$(FLAGSDIR)/$(CORE_PATH)

PROJECTS=$(CORE_PROJECT) $(JINJA2_PROJECT)

# virtualenv
VIRUALENV=venv_impaf
ACTIVATE=source $(VIRUALENV)/bin/activate

all: $(PROJECTS)

$(CORE_PROJECT): $(CORE_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(CORE_PATH) && python setup.py develop
	@touch $(CORE_PROJECT)

venv_impaf:
	virtualenv $@
	mkdir $(FLAGSDIR)
