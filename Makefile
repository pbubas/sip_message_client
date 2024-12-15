.PHONY: build upload clean

build:
	poetry build

upload:
	poetry publish --build --username __token__ --password ${PYPI_TOKEN}

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info


