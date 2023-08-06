# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nisystemlink',
 'nisystemlink.clients',
 'nisystemlink.clients.core',
 'nisystemlink.clients.core._internal',
 'nisystemlink.clients.core._uplink',
 'nisystemlink.clients.dataframe',
 'nisystemlink.clients.dataframe.models',
 'nisystemlink.clients.tag',
 'nisystemlink.clients.tag._core',
 'nisystemlink.clients.tag._http']

package_data = \
{'': ['*'], 'nisystemlink': ['stubs/*']}

install_requires = \
['Events>=0.4,<0.5',
 'aenum>=3.1.11,<4.0.0',
 'httpx>=0.23.0,<0.24.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'uplink>=0.9.7,<0.10.0']

setup_kwargs = {
    'name': 'nisystemlink-clients',
    'version': '1.0.0',
    'description': 'NI-SystemLink Python API',
    'long_description': '===========  ====================================================\nInfo         NI SystemLink API Clients for Python\nAuthor       National Instruments\n===========  ====================================================\n\nAbout\n=====\nThe **nisystemlink-clients** package contains an API (Application Programming\nInterface) for `SystemLink <https://ni.com/systemlink>`_ that uses HTTP to\ninteract with a SystemLink Server. The package is implemented in Python. NI\ncreated and supports this package.\n\n.. image:: https://badge.fury.io/py/nisystemlink-clients.svg\n    :target: https://badge.fury.io/py/nisystemlink-clients\n\nRequirements\n============\n**nisystemlink-clients** has the following requirements:\n\n* A SystemLink Server installation or a\n  `SystemLink Cloud <https://www.systemlinkcloud.com/>`_ account to connect to\n* CPython 3.8+\n\n.. _installation_section:\n\nInstallation\n============\nTo install **nisystemlink-clients**, use one of the following methods:\n\n1. `pip <https://pypi.python.org/pypi/pip>`_::\n\n   $ python -m pip install nisystemlink-clients\n\n2. **easy_install** from `setuptools <https://pypi.python.org/pypi/setuptools>`_::\n\n   $ python -m easy_install nisystemlink-clients\n\n.. _usage_section:\n\nUsage\n=====\nRefer to the `documentation <https://python-docs.systemlink.io>`_\nfor detailed information on how to use **nisystemlink-clients**.\n\n.. _support_section:\n\nSupport / Feedback\n==================\nThe **nisystemlink-clients** package is supported by NI. For support for\n**nisystemlink-clients**, open a request through the NI support portal at\n`ni.com <https://www.ni.com>`_.\n\nBugs / Feature Requests\n=======================\nTo report a bug or submit a feature request, please use the\n`GitHub issues page <https://github.com/ni/nisystemlink-clients-python/issues>`_.\n\nDocumentation\n=============\nTo view the documentation, visit the\n`nisystemlink.clients Documentation Page <https://python-docs.systemlink.io>`_.\n\nChangelog\n=============\nTo view the changelog, visit the\n`GitHub repository CHANGELOG <https://github.com/ni/nisystemlink-clients-python/blob/master/CHANGELOG.md>`_.\n\nLicense\n=======\n**nisystemlink-clients** is licensed under an MIT-style license (see `LICENSE\n<LICENSE>`_).  Other incorporated projects may be licensed under different\nlicenses. All licenses allow for non-commercial and commercial use.\n',
    'author': 'National Instruments',
    'author_email': 'None',
    'maintainer': 'Carson Moore',
    'maintainer_email': 'carson.moore@ni.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
