# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpg_keymanager',
 'gpg_keymanager.bin',
 'gpg_keymanager.bin.commands',
 'gpg_keymanager.keys',
 'gpg_keymanager.platform',
 'gpg_keymanager.store']

package_data = \
{'': ['*']}

install_requires = \
['pathlib-tree>=2,<3']

entry_points = \
{'console_scripts': ['gpg-keymanager = gpg_keymanager.bin.gpg_keymanager:main']}

setup_kwargs = {
    'name': 'gpg-keymanager',
    'version': '1.1.0',
    'description': 'gpg pass password store keyring management',
    'long_description': '![Unit Tests](https://github.com/hile/gpg-keymanager/actions/workflows/unittest.yml/badge.svg)\n![Style Checks](https://github.com/hile/gpg-keymanager/actions/workflows/lint.yml/badge.svg)\n\n# GPG keyring and password store key management utilities\n\nThis python module contains utilities to manage user PGP keys and encryption keys\nused for encryping items in GNU password store.\n\n## PGP key filesystem directory\n\nLoading PGP public keys from a filesystem directory can be used to allow teams to\npublish member PGP keys without using key servers. This procedure is not secure by\nitself but is reasonable enough when combined with access controls to the directory\nand some external identity management tools like LDAP lookups.\n\nAny PGP key imported from such access controlled filesystem directory or git\nrepository should still be checked with PGP fingerprint as usual.\n\n## GNU password store encryption key management\n\nThis utility helps managing encryption keys used in *pass* password store, which can\nencrypt items in the store to one or multiple PGP key IDs per folder.\n',
    'author': 'Ilkka Tuohela',
    'author_email': 'hile@iki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hile/gpg-keymanager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
