# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berhoel',
 'berhoel.ctitools',
 'berhoel.ctitools.cti2bibtex',
 'berhoel.ctitools.cti2bibtex.tests',
 'berhoel.ctitools.tests']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=65.3.0,<66.0.0']

entry_points = \
{'console_scripts': ['cti2bibtex = berhoel.ctitools.cti2bibtex:main',
                     'cti_statistics = berhoel.ctitools:cti_statistics']}

setup_kwargs = {
    'name': 'ctitools',
    'version': '0.4.0',
    'description': "Work with cti index files for the Heise papers c't and iX",
    'long_description': 'Ctitools\n========\n\nWork with cti index files for the Heise papers c’t and iX\n\nDescription\n-----------\n\nThis project provides diffrent tool for processing index files from\nHeise papers c’t and iX.\n\nSaving the current base dataset, downloaded from Heise and extractng to\ndata, the command\n\n.. code:: console\n\n  > cti2bibtex data/inhalt.frm result.bibtex\n\ncreates a ``.bib`` file with 82100 entries. Importing this result in\nZotero took more than 28h and use more than 7GB of RAM.\n\nInstallation\n------------\n\n.. code:: console\n\n  > pip install git+https://gitlab.com/berhoel/python/ctitools.git\n\nDocumentation\n-------------\n\nDocumentation can be found `here <https://python.höllmanns.de/ctitools/>`_\n\nAuthors\n-------\n\n- Berthold Höllmann <berthold@xn--hllmanns-n4a.de>\n\nProject status\n--------------\n\nThe projects works for converting the `cti` and `frm` file, provided\nby Heise, to `bib` files.\n',
    'author': 'Berthold Höllmann',
    'author_email': 'berthold@xn--hllmanns-n4a.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://python.xn--hllmanns-n4a.de/ctitools/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
