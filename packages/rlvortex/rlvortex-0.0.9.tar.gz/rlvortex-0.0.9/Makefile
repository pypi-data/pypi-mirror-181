# 4. upload package to pypi repository
# install/update tools used to package build and install
tool-update:
# 1. install/ update build tool to package build
	python3 -m pip install --upgrade build
# 2. install/ update twine for package uploading
	python3 -m pip install --upgrade twine
# build package to local, dist/*
build:
	@echo "uploading to dist/" 
	python3 -m build
# upload built package to test pypi
upload-test:
	@echo "upload-test option is deprecated due to gym package is obslete in testpypi "
	# @echo "uploading to test pypi" 
	# twine upload --verbose -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkYTFjZWZiODEtNzQxZS00M2RjLTgyNGYtMWRiYWI4ZjE2MjU3AAIqWzMsIjhlZDU2NjIxLWQ1OGYtNGY3YS1iOGI1LWMzODhjMmI3ZDRhMCJdAAAGIK9i2nvQIbsMDQsyE6BAlt5wmTH8xsujNftl9bCB4Ab- -r testpypi dist/* 
# upload built package to pypi
upload:
	@echo "uploading to pypi" 
	twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDM3MzUzY2JkLTIyNjQtNGFkMS04MTFkLWM0Mzc0MWFlNDU0ZQACKlszLCJjNGY5ZWJjZC1kNzdjLTQ2MjYtYjNhOC1hYzRkYjA4NmY3NjMiXQAABiClVpqRQr23DY1nRGUUvS5QqZdX7WhtShVhF3XgaZPqfg dist/*
# excute tool-update, build, and upload to pypi
all:
	make clean
	make tool-update
	make build
	make upload
	make clean
# excute tool-update, build, and upload to pypi
all-test:
	@echo "all-test option is deprecated due to gym package is obslete in testpypi "
	# make clean
	# make tool-update
	# make build
	# make upload-test
	# make clean
install-test:
	@echo "install-test option is deprecated due to gym package is obslete in testpypi"
	# pip install -i https://test.pypi.org/simple/ rlvortex
install:
	pip install rlvortex
install-local:
	python -m pip install .
.PHONY: clean
clean: 
	rm -rf dist/