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

mkdocs_github_deploy() {
    mkdocs gh-deploy
}

"$@"
