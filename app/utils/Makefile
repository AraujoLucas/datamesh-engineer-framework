.PHONY: help clean clean-builds coverage lint test

.DEFAULT: help

help:
	@echo "make clean"
	@echo "			prepare development environment, use only once"
	@echo "make clean-build"
	@echo "			clean all build artifacts"
	@echo "make coverage"
	@echo "			generate code coverage report"
	@echo "make lint"
	@echo "			run lint"
	@echo "make test"
	@echo "			run test"

clean:
	@echo "Cleaning development environment..."
	# Comandos para limpar arquivos temporários, caches, etc.
	# Por exemplo:
	# rm -rf tmp/* .cache/*

clean-builds:
	@echo "Cleaning all build artifacts..."
	# Comandos para limpar todos os artefatos de build gerados
	# Por exemplo:
	# rm -rf build/*

coverage:
	@echo "Generating code coverage report..."
	# Comandos para gerar relatórios de cobertura de código
	# Por exemplo:
	# coverage run --source=my_project -m pytest
	# coverage report -m

lint:
	@echo "Running lint..."
	# Comandos para executar a verificação de código estático (linting)
	# Por exemplo:
	# pylint my_project/*.py

test:
	@echo "Running tests..."
	# Comandos para executar testes automatizados
	# Por exemplo:
	# pytest tests/*.py