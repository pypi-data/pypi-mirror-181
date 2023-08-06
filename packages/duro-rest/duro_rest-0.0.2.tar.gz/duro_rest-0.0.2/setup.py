from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'duro_rest',
    version = '0.0.2',
    license = 'Mozilla Public License 2.0',
    description = 'An API client for the Duro REST API',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = ['duro_rest'],
    classifiers = [
      'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)'
    ],
    maintainer = 'augustuswm',
    maintainer_email = 'augustus@oxidecomputer.com',
    install_requires = [
      'requests'
    ]
)