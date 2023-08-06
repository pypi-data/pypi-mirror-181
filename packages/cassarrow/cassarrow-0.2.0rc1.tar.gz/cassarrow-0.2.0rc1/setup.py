# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cassarrow']

package_data = \
{'': ['*']}

install_requires = \
['cassandra-driver>=3.0.0',
 'pyarrow>=8.0.0',
 'pybind11>=2.10.1',
 'wheel>=0.37.0']

setup_kwargs = {
    'name': 'cassarrow',
    'version': '0.2.0rc1',
    'description': 'Apache Arrow adapter for the Cassandra python driver',
    'long_description': '# Cassarrow\n\nArrow based Cassandra python driver. \n\n## TLDR;\n\nSpeed up the cassandra python driver using C++ to parse cassandra queries data as [Apache Arrow](https://arrow.apache.org/) tables.\n\nKey features:\n* 20x speed up in the parsing of results\n* 14x less memory\n* Support for most native types, UDT, List and Set\n\n## Getting Started\n\n### Installation\n\n```shell\npip install cassarrow\n```\n\n### Usage\n\n```python\nimport cassarrow\nimport pyarrow as pa\n\n# ...\n\nwith cassarrow.install_cassarrow(session) as cassarrow_session:\n    table: pa.Table = cassarrow.result_set_to_table(cassarrow_session.execute("SELECT * FROM my_table"))\n```\n\n## Type Mapping\n\n### Native Types\n\n| Cassandra   | pyarrow              | Note         |\n|:------------|:---------------------|:-------------|\n| ascii       | `pa.string()`        |              |\n| bigint      | `pa.int64()`         |              |\n| blob        | `pa.binary()`        |              |\n| boolean     | `pa.bool_()`         |              |\n| counter     |                      | TODO         |\n| date        | `pa.date32()`        |              |\n| decimal     |                      | Incompatible |\n| double      | `pa.float64()`       |              |\n| duration    | `pa.duration("ns")`  |              |\n| float       | `pa.float32()`       |              |\n| inet        |                      | TODO         |\n| int         | `pa.int32()`         |              |\n| smallint    | `pa.int16()`         |              |\n| text        | `pa.string()`        |              |\n| time        | `pa.time64("ns")`    |              |\n| timestamp   | `pa.timestamp("ms")` |              |\n| timeuuid    | `pa.binary(16)`      |              |\n| tinyint     | `pa.int8()`          |              |\n| uuid        | `pa.binary(16)`      |              |\n| varchar     | `pa.string()`        |              |\n| varint      |                      | Incompatible |\n\n## Collections / UDT\n\n| Cassandra   | pyarrow     | Note   |\n|:------------|:------------|:-------|\n| list        | `pa.list_`  |        |\n| map         | `pa.map_`   |        |\n| set         | `pa.list_`  |        |\n| udt         | `pa.struct` |        |',
    'author': '0x26res',
    'author_email': '0x26res@gamil.com',
    'maintainer': '0x26res',
    'maintainer_email': '0x26res@gmail.com',
    'url': 'https://github.com/0x26res/cassarrow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
