.PHONY: help clean server

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean                 delete all compiled python and backup files"
	@echo "  server                start the development server"
	@echo "  shell                 start a development shell"

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

server:
	@(python manage.py runserver)

shell:
	@(python manage.py shell)
