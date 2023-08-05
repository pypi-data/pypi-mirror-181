PYTHON_VERSION = 3.9
PYTHONNOUSERSITE = /dev/null
PIPENV := $(shell which pipenv 2>/dev/null)

.PHONY: all
all:
	@echo "Run 'make publish_testpypi' or 'make publish' or check/read makefile"

.PHONY: init
init:
	@: $(PIPENV) --rm 2>/dev/null || echo ""
	$(PIPENV) --python $(PYTHON_VERSION)

.PHONY:
pip_install:
	source $(shell ${PIPENV} --venv)/bin/activate && pip install .[test,dev]


.PHONY:
get_saxon_he: src/saxon_he
	rm -rf src/saxon_he
	mkdir -p src/saxon_he
	wget -q -O /tmp/saxonhe.zip 'https://sourceforge.net/projects/saxon/files/Saxon-HE/11/Java/SaxonHE11-4J.zip/download'
	unzip -n  -q /tmp/saxonhe.zip -d src/saxon_he

.PHONY:
build: clean init pip_install get_saxon_he
	source $(shell ${PIPENV} --venv)/bin/activate && python3 -m build

.PHONY:
publish_test: build
	source $(shell ${PIPENV} --venv)/bin/activate && python3 -m twine upload --repository testpypi dist/*

.PHONY:
publish: build
	source $(shell ${PIPENV} --venv)/bin/activate && python3 -m twine upload --repository pypi dist/*

.PHONY:
clean:
	rm -rf dist build