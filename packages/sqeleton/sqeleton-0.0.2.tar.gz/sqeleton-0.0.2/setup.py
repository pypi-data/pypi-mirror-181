# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqeleton', 'sqeleton.abcs', 'sqeleton.databases', 'sqeleton.queries']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1,<9.0',
 'dsnparse',
 'rich',
 'runtype>=0.2.6,<0.3.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{'clickhouse': ['clickhouse-driver'],
 'duckdb': ['duckdb>=0.6.0,<0.7.0'],
 'mysql': ['mysql-connector-python==8.0.29'],
 'postgresql': ['psycopg2'],
 'presto': ['presto-python-client'],
 'snowflake': ['snowflake-connector-python>=2.7.2,<3.0.0', 'cryptography'],
 'trino': ['trino>=0.314.0,<0.315.0']}

entry_points = \
{'console_scripts': ['sqeleton = sqeleton.__main__:main']}

setup_kwargs = {
    'name': 'sqeleton',
    'version': '0.0.2',
    'description': 'Python library for querying SQL databases',
    'long_description': '# Sqeleton\n\n**Under construction!**\n\nPython library for querying SQL databases.\n\nIt consists of -\n\n- A fast and concise query builder, inspired by PyPika and SQLAlchemy\n\n- A modular database interface, with drivers for a long list of SQL databases.\n\n### Databases we support\n\n- PostgreSQL >=10\n- MySQL\n- Snowflake\n- BigQuery\n- Redshift\n- Oracle\n- Presto\n- Databricks\n- Trino\n- Clickhouse\n- Vertica\n- DuckDB >=0.6\n- SQLite (coming soon)\n\n\n### Built for performance\n\n- Multi-threaded by default - introduce ThreadLocalInterpreter\n\n- No ORM - Nice for beginners, but encourages bad behavior\n\n## Type-aware\n\nType validation when building expressions (and make sure columns exist)\n\nAllows type introspection\n\n# TODO\n\n- Transactions\n\n- Indexes\n\n- Date/time expressions\n\n- Window functions\n\n## Possible plans for the future (not determined yet)\n\n- Cache compilation of repetitive queries for even faster query-building\n\n- Compile control flow, functions\n\n- Define tables using type-annotated classes (SQLModel style)\n',
    'author': 'Erez Shinan',
    'author_email': 'erezshin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/datafold/sqeleton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
