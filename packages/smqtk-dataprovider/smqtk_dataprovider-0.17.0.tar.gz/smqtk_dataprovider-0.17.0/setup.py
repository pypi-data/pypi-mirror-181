# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smqtk_dataprovider',
 'smqtk_dataprovider.impls',
 'smqtk_dataprovider.impls.data_element',
 'smqtk_dataprovider.impls.data_set',
 'smqtk_dataprovider.impls.key_value_store',
 'smqtk_dataprovider.interfaces',
 'smqtk_dataprovider.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1', 'smqtk-core>=0.19']

extras_require = \
{':python_version < "3.8"': ['numpy>=1.21.1'],
 ':python_version >= "3.8"': ['numpy>=1.23.5'],
 'filemagic': ['file-magic>=0.4.0,<0.5.0'],
 'girder': ['girder-client>=3.1.3,<4.0.0'],
 'psql': ['psycopg2-binary>=2.9.5,<3.0.0']}

entry_points = \
{'smqtk_plugins': ['smqtk_dataprovider.impls.data_element.file = '
                   'smqtk_dataprovider.impls.data_element.file',
                   'smqtk_dataprovider.impls.data_element.girder = '
                   'smqtk_dataprovider.impls.data_element.girder',
                   'smqtk_dataprovider.impls.data_element.hbase = '
                   'smqtk_dataprovider.impls.data_element.hbase',
                   'smqtk_dataprovider.impls.data_element.matrix = '
                   'smqtk_dataprovider.impls.data_element.matrix',
                   'smqtk_dataprovider.impls.data_element.memory = '
                   'smqtk_dataprovider.impls.data_element.memory',
                   'smqtk_dataprovider.impls.data_element.psql = '
                   'smqtk_dataprovider.impls.data_element.psql',
                   'smqtk_dataprovider.impls.data_element.url = '
                   'smqtk_dataprovider.impls.data_element.url',
                   'smqtk_dataprovider.impls.data_set.file = '
                   'smqtk_dataprovider.impls.data_set.file',
                   'smqtk_dataprovider.impls.data_set.kvstore_backed = '
                   'smqtk_dataprovider.impls.data_set.kvstore_backed',
                   'smqtk_dataprovider.impls.data_set.memory = '
                   'smqtk_dataprovider.impls.data_set.memory',
                   'smqtk_dataprovider.impls.data_set.psql = '
                   'smqtk_dataprovider.impls.data_set.psql',
                   'smqtk_dataprovider.impls.key_value_store.memory = '
                   'smqtk_dataprovider.impls.key_value_store.memory',
                   'smqtk_dataprovider.impls.key_value_store.postgres = '
                   'smqtk_dataprovider.impls.key_value_store.postgres']}

setup_kwargs = {
    'name': 'smqtk-dataprovider',
    'version': '0.17.0',
    'description': 'SMQTK Data provision abstractions and implementations',
    'long_description': '# SMQTK - Data Providers\n\n## Intent\nThis package builds on top of SMQTK-Core to provide data structures that are\nabstractions around data and where it is fundamentally stored.\n\n## Documentation\nYou can build the sphinx documentation locally for the most up-to-date\nreference:\n```bash\n# Install dependencies\npoetry install\n# Navigate to the documentation root.\ncd docs\n# Build the docs.\npoetry run make html\n# Open in your favorite browser!\nfirefox _build/html/index.html\n```\n',
    'author': 'Kitware, Inc.',
    'author_email': 'smqtk-developers@kitware.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Kitware/SMQTK-Dataprovider',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
