.PHONY: help clean

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean                 delete all compiled python and backup files"

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
