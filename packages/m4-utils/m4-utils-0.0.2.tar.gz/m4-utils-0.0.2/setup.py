# -*- coding: utf-8 -*-
"""
setup.py
------------
c50 wrapper setup script.
"""
from setuptools import setup, find_packages
# builds the project dependency list
install_requires = None
with open('requirements.txt', 'r') as f:
    install_requires = f.readlines()
    install_requires = list(
        map(
            lambda x: x.replace('==', '>=').replace('\\','').strip(),
            filter(
                lambda x: not x.strip().startswith('--hash=') and not x.strip().startswith('# via -r'),
                install_requires
            )
        )
    )

#read version file
VERSION = None
with open('VERSION', 'r') as f:
    VERSION = f.read().strip()

# setup function call
setup(
    name="m4-utils",
    version=VERSION,
    author="SERVICE PREVENTION",
    author_email="",
    description=(
        "Biblioteca com funções de uso comum em projetos de aprendizado de máquina e ciencia de dados."
    ),
    keywords=["Utility Functions", "Data Science"],
    # Install project dependencies
    install_requires=install_requires,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md', "*.json", '*.zip'],
    },
    include_package_data=True,
    packages=find_packages(exclude=["*tests"]),
)
