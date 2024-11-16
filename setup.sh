#!/bin/bash

APP_HOME=django_util

# https://jacobtomlinson.dev/posts/2020/versioning-and-formatting-your-python-code/
versioneer_cleanup() {
    rm -f .gitattributes
    rm -f versioneer.py
    rm -f "$APP_HOME"/__init__.py
    rm -f "$APP_HOME"/_version.py
}

versioneer_setup() {
    touch "$APP_HOME"/__init__.py
    # prepare setup.cfg, setup.py
    versioneer install --vendor
}

# https://realpython.com/python-project-documentation-with-mkdocs/#step-3-write-and-format-your-docstrings
mkdocs_setup() {
    mkdocs new .
}

mkdocs_rebuild() {
    rm -rf site
    mkdocs build
}

mkdocs_github_deploy() {
    mkdocs gh-deploy
}

build_pypi() {
    rm -rf build
    rm -rf dist
    rm -rf django_util.egg-info
    rm -rf django_util-*
    # Build distribution
    python setup.py sdist bdist_wheel
}

upload_pypi() {
    # Upload to Test PyPi
    # python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
    # Upload to PyPi
    twine upload dist/*
}

"$@"
