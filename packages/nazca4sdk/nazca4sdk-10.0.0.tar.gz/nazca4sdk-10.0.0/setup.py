
import pathlib
from setuptools import setup, find_packages
import pkg_resources

HERE = pathlib.Path(__file__).parent
VERSION = '10.0.00'
PACKAGE_NAME = 'nazca4sdk'
AUTHOR = 'Nazca4.0'
AUTHOR_EMAIL = ''
URL = 'https://www.apagroup.pl'
LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Nazca4 SDK'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]
setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      include_package_data=True,
      install_requires=install_requires,
      packages=find_packages()
      )