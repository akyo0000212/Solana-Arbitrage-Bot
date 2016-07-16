help:
	@echo "build - Build package"
	@echo "install - Install package to local system"
	@echo "clean - Clean built artifacts"
	@echo "test - Run test suite with coverage"

build:
	python setup.py build
	python setup.py bdist_wheel

install:
	pip install dist/*.whl --upgrade --force-reinstall --no-deps
	python setup.py clean

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf ./build ./dist ./*.egg-info
