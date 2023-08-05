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
    'version': '0.0.3',
    'description': 'Databricks SQL framework, easy to learn, fast to code, ready for production.',
    'long_description': '# Databricks SQL\n\nDatabricks SQL framework, easy to learn, fast to code, ready for production.\n\n## Installation\n\n```shell\n$ pip install databricks-sql\n```\n\n## Configuration\n\n```python\nfrom databricks_sql.client import Configuration\n\nCONFIGURATION = Configuration.instance(\n    access_token="",\n    command_directory="",\n    http_path="",\n    server_hostname="",\n)\n```\n\n## Usage\n\nDatabricks SQL usage description:\n\n### Execute\n\n```python\nfrom databricks_sql.client import Database\n\nwith Database() as connection:\n    (\n        connection\n        .execute(\n            """\n                CREATE TABLE IF NOT EXISTS catalog.schema.table (\n                    id STRING NOT NULL,\n                    name STRING NOT NULL,\n                    description STRING,\n                    CONSTRAINT table_primary_key PRIMARY KEY(id)\n                ) USING DELTA\n            """,\n            parameters=None,\n            skip_load=True,\n        )\n    )\n```\n\n### Insert\n\n```python\nfrom databricks_sql.client import Database\n\nwith Database() as connection:\n    (\n        connection\n        .insert("catalog.schema.table")\n        .set("id", "994238a4-8c18-436a-8c06-29ec89c4c056")\n        .set("name", "Name")\n        .set("description", "Description")\n        .execute()\n    )\n```\n\n### Paging\n\n#### Paging with where condition\n\n```python\nfrom databricks_sql.client import Database\n\nwith Database() as connection:\n    (\n        connection\n        .select("catalog.schema.table")\n        .fields("id", "name", "description")\n        .where("name", "%Databricks%", operator="LIKE")\n        .order_by("id")\n        .paging(0, 10)\n    )\n```\n\n#### Paging without where condition\n\n```python\nfrom databricks_sql.client import Database\n\nwith Database() as connection:\n    (\n        connection\n        .select("catalog.schema.table")\n        .paging(0, 10)\n    )\n```\n\n### Select\n\n#### Fetch all\n\n```python\nfrom databricks_sql.client import Database\n\nwith Database() as connection:\n    (\n        connection\n        .select("test")\n        .execute()\n        .fetch_all()\n    )\n```\n\n#### Fetch many\n\n```python\nfrom databricks_sql.client import Database\n\nwith Database() as connection:\n    (\n        connection\n        .select("test")\n        .execute()\n        .fetch_many(1)\n    )\n```\n\n#### Fetch one\n\n```python\nfrom databricks_sql.client import Database\n\nwith Database() as connection:\n    (\n        connection\n        .select("test")\n        .execute()\n        .fetch_one()\n    )\n```\n\n#### Select by file\n\n```python\nfrom databricks_sql.client import Database\n\nwith Database() as connection:\n    (\n        connection\n        .execute("read_by_id", {"id": "994238a4-8c18-436a-8c06-29ec89c4c056"})\n        .fetch_one()\n    )\n```\n\n#### Select by command\n\n```python\nfrom databricks_sql.client import Database\n\nwith Database() as connection:\n    (\n        connection\n        .execute("SELECT id, name, description FROM catalog.schema.table WHERE id = %(id)s", {"id": "994238a4-8c18-436a-8c06-29ec89c4c056"})\n        .fetch_one()\n    )\n```\n\n## License\n\nThis project is licensed under the terms of the [Apache License 2.0](https://github.com/bernardocouto/databricks-sql/blob/main/LICENSE).\n',
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
