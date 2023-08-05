# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databricks_sql']

package_data = \
{'': ['*']}

install_requires = \
['databricks-sql-connector==2.2.1', 'pystache==0.6.0']

setup_kwargs = {
    'name': 'databricks-sql',
    'version': '0.0.2',
    'description': 'Databricks SQL framework, easy to learn, fast to code, ready for production.',
    'long_description': '# Databricks SQL\n\nDatabricks SQL framework, easy to learn, fast to code, ready for production.\n\n## Installation\n\n```shell\n$ pip install databricks-sql\n```\n\n## Configuration\n\n```python\nfrom databricks_sql.client import Configuration\n\nCONFIGURATION = Configuration.instance(\n    access_token="",\n    command_directory="",\n    http_path="",\n    server_hostname="",\n)\n```\n\n## License\n\nThis project is licensed under the terms of the [Apache License 2.0](https://github.com/bernardocouto/databricks-sql/blob/main/LICENSE).\n',
    'author': 'Bernardo Couto',
    'author_email': 'bernardocouto@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bernardocouto/databricks-sql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
