FLAGSDIR=flags

# core
CORE_PATH=core
CORE_PROJECT=$(FLAGSDIR)/$(CORE_PATH)

# jinja2
JINJA2_PATH=jinja2
JINJA2_PROJECT=$(FLAGSDIR)/$(JINJA2_PATH)

# haml
HAML_PATH=haml
HAML_PROJECT=$(FLAGSDIR)/$(HAML_PATH)

# sqlalchemy
SQLALCHEMY_PATH=sqlalchemy
SQLALCHEMY_PROJECT=$(FLAGSDIR)/$(SQLALCHEMY_PATH)

# alembic
ALEMBIC_PATH=alembic
ALEMBIC_PROJECT=$(FLAGSDIR)/$(ALEMBIC_PATH)

# fanstatic
FANSTATIC_PATH=fanstatic
FANSTATIC_PROJECT=$(FLAGSDIR)/$(FANSTATIC_PATH)

# formskit
FORMSKIT_PATH=formskit
FORMSKIT_PROJECT=$(FLAGSDIR)/$(FORMSKIT_PATH)

# flash messages
FLASHMSG_PATH=flashmsg
FLASHMSG_PROJECT=$(FLAGSDIR)/$(FLASHMSG_PATH)

# auth
AUTH_PATH=auth
AUTH_PROJECT=$(FLAGSDIR)/$(AUTH_PATH)

# example
EXAMPLE_PATH=example
EXAMPLE_PROJECT=$(FLAGSDIR)/$(EXAMPLE_PATH)

PROJECTS=$(CORE_PROJECT) $(JINJA2_PROJECT) $(HAML_PROJECT) $(SQLALCHEMY_PROJECT) $(ALEMBIC_PROJECT) $(FANSTATIC_PROJECT) $(FORMSKIT_PROJECT) $(FLASHMSG_PROJECT) $(AUTH_PROJECT) $(EXAMPLE_PROJECT)
UPDATE=$(FLAGSDIR)/update

# virtualenv
VIRUALENV=venv_impaf
ACTIVATE=source $(VIRUALENV)/bin/activate

all: $(UPDATE) $(PROJECTS)

$(UPDATE): .gitmodules
	git submodule init
	git submodule update
	touch $(UPDATE)

$(CORE_PROJECT): $(CORE_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(CORE_PATH) && python setup.py develop
	@touch $(CORE_PROJECT)

$(JINJA2_PROJECT): $(JINJA2_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(JINJA2_PATH) && python setup.py develop
	@touch $(JINJA2_PROJECT)

$(EXAMPLE_PROJECT): $(EXAMPLE_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(EXAMPLE_PATH) && python setup.py develop
	@touch $(EXAMPLE_PROJECT)

$(HAML_PROJECT): $(HAML_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(HAML_PATH) && python setup.py develop
	@touch $(HAML_PROJECT)

$(SQLALCHEMY_PROJECT): $(SQLALCHEMY_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(SQLALCHEMY_PATH) && python setup.py develop
	@touch $(SQLALCHEMY_PROJECT)

$(ALEMBIC_PROJECT): $(ALEMBIC_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(ALEMBIC_PATH) && python setup.py develop
	@touch $(ALEMBIC_PROJECT)

$(FANSTATIC_PROJECT): $(FANSTATIC_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(FANSTATIC_PATH) && python setup.py develop
	@touch $(FANSTATIC_PROJECT)

$(FORMSKIT_PROJECT): $(FORMSKIT_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(FORMSKIT_PATH) && python setup.py develop
	@touch $(FORMSKIT_PROJECT)

$(FLASHMSG_PROJECT): $(FLASHMSG_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(FLASHMSG_PATH) && python setup.py develop
	@touch $(FLASHMSG_PROJECT)

$(AUTH_PROJECT): $(AUTH_PATH)/setup.py venv_impaf
	$(ACTIVATE) && cd $(AUTH_PATH) && python setup.py develop
	@touch $(AUTH_PROJECT)

venv_impaf:
	virtualenv $@
	mkdir -p $(FLAGSDIR)

serve: $(UPDATE) $(PROJECTS)
	$(ACTIVATE) && cd example && pserve frontend.ini --reload

test: $(UPDATE) $(PROJECTS)
	$(ACTIVATE) && py.test
