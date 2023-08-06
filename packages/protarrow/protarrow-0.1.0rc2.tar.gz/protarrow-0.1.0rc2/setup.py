# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protarrow']

package_data = \
{'': ['*']}

install_requires = \
['googleapis-common-protos>=1.53.0', 'protobuf>=3.20.1', 'pyarrow>=8.0.0']

setup_kwargs = {
    'name': 'protarrow',
    'version': '0.1.0rc2',
    'description': 'Convert from protobuf to arrow and back',
    'long_description': '[![PyPI Version][pypi-image]][pypi-url]\n[![Python Version][versions-image]][versions-url]\n[![Github Stars][stars-image]][stars-url]\n[![codecov][codecov-image]][codecov-url]\n[![Build Status][build-image]][build-url]\n[![Documentation][doc-image]][doc-url]\n[![License][license-image]][license-url]\n\n# Protarrow\n\n**Protarrow** is a python library for converting from protobuf to arrow and back.\n\nIt is used at [Tradewell Technologies](https://www.tradewelltech.co/), \nto share date between transactional and analytical applications,\nwith little boilerplate code and zero data loss.\n\n# Installation\n\n```shell\npip install protarrow\n```\n\n# Usage\n\nTaking a simple protobuf:\n\n```protobuf\nmessage MyProto {\n  string name = 1;\n  int32 id = 2;\n  repeated int32 values = 3;\n}\n```\n\nIt can be converted to a `pyarrow.Table`:\n\n```python\nimport protarrow\n\nmy_protos = [\n    MyProto(name="foo", id=1, values=[1, 2, 4]),\n    MyProto(name="bar", id=2, values=[3, 4, 5]),\n]\n\ntable = protarrow.messages_to_table(my_protos, MyProto)\n```\n\n\n| name   |   id | values   |\n|:-------|-----:|:---------|\n| foo    |    1 | [1 2 4]  |\n| bar    |    2 | [3 4 5]  |\n\nAnd the table can be converted back to proto:\n\n```python\nprotos_from_table = protarrow.table_to_messages(table, MyProto)\n```\n\nSee the [documentation](https://protarrow.readthedocs.io/en/latest/)\n\n\n<!-- Badges: -->\n\n[pypi-image]: https://img.shields.io/pypi/v/protarrow\n[pypi-url]: https://pypi.org/project/protarrow/\n[build-image]: https://github.com/tradewelltech/protarrow/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/tradewelltech/protarrow/actions/workflows/build.yaml\n[stars-image]: https://img.shields.io/github/stars/tradewelltech/protarrow\n[stars-url]: https://github.com/tradewelltech/protarrow\n[versions-image]: https://img.shields.io/pypi/pyversions/protarrow\n[versions-url]: https://pypi.org/project/protarrow/\n[doc-image]: https://readthedocs.org/projects/protarrow/badge/?version=latest\n[doc-url]: https://protarrow.readthedocs.io/en/latest/?badge=latest\n[license-image]: http://img.shields.io/:license-Apache%202-blue.svg\n[license-url]: https://github.com/tradewelltech/protarrow/blob/master/LICENSE.txt\n[codecov-image]: https://codecov.io/gh/tradewelltech/protarrow/branch/master/graph/badge.svg?token=XMFH27IL70\n[codecov-url]: https://codecov.io/gh/tradewelltech/protarrow\n',
    'author': 'Tradewell Tech',
    'author_email': 'engineering@tradewelltech.co',
    'maintainer': '0x26res',
    'maintainer_email': '0x26res@gmail.com',
    'url': 'https://github.com/tradewelltech/protarrow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
