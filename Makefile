.PHONY: build upload clean

tag:
    git tag v$(shell poetry version -s)
    git push origin v$(shell poetry version -s)

build:
	poetry build

upload:
	poetry publish --build --username __token__ --password ${PYPI_TOKEN}

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

