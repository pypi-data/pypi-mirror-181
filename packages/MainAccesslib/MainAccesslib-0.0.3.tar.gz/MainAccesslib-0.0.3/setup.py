__author__ = 'Jordi Arellano'
__copyright__ = 'Copyleft 2021'
__date__ = '05/04/22'
__credits__ = ['Jordi Arellano', ]
__license__ = 'CC0 1.0 Universal'
__version__ = '0.0.3'
__maintainer__ = 'Jordi Arellano'
__email__ = 'jordiarellano1996@gmail.com'

from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
requirementPath = os.path.join(here, 'requirements.txt')
install_requires = []  # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

# Read README and CHANGES files for the long description

with open(os.path.join(here, 'README.md')) as fh:
    long_description = fh.read()

setup(name="MainAccesslib",
      include_package_data=True,
      version=__version__,
      description="This lib controls photonai camera.",
      long_description_content_type="text/markdown",
      long_description=long_description,
      python_requires='>=3',
      packages=["MainAccesslib", "MainAccesslib.characteritzation", "MainAccesslib.characteritzation.logic",
                "MainAccesslib.equalization", "MainAccesslib.equalization.algorithm"],
      # package_data={'': [f"{os.path.join(here, 'PBaccesslib/data/*.npy')}", ]},
      license="CC0 1.0 Universal",
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Programming Language :: Python :: 3",
      ],
      setup_requires=['wheel'],
      install_requires=["typing-extensions==4.1.1", "DDBitConvertAccesslib==0.1.0", "DDBridgeAccesslib==0.1.0",
                        "DDExcelAccesslib==0.1.1", "et-xmlfile==1.1.0", "numpy==1.23.4", "openpyxl==3.0.10",
                        "pandas==1.5.1", "python-dateutil==2.8.2", "pytz==2022.6", "six==1.16.0"],
      )
