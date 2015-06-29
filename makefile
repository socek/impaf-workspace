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

# example
EXAMPLE_PATH=example
EXAMPLE_PROJECT=$(FLAGSDIR)/$(EXAMPLE_PATH)

PROJECTS=$(CORE_PROJECT) $(JINJA2_PROJECT) $(HAML_PROJECT) $(SQLALCHEMY_PROJECT) $(ALEMBIC_PROJECT) $(FANSTATIC_PROJECT) $(EXAMPLE_PROJECT)
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

venv_impaf:
	virtualenv $@
	mkdir -p $(FLAGSDIR)

serve: $(UPDATE) $(PROJECTS)
	cd example && pserve frontend.ini --reload

test: $(UPDATE) $(PROJECTS)
	py.test --cov impaf --cov implugin --cov impex --cov haml --cov sqlalchemy
