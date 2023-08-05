# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mbus_gem_decoder',
 'mbus_gem_decoder.conversion',
 'mbus_gem_decoder.conversion.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mbus-gem-decoder',
    'version': '0.1.0',
    'description': 'MBUS-GEM decoder',
    'long_description': '# mbusgemdecoder package\nDecode MBUS-GEM register data into human-readable JSON.\n\n## Introduction\nThe goal of `mbusgemdecoder` package is to convert a list of ten integer values into human-readable data object. `mbusgemdecoder` package automatically detects the type (`MBUS-GEM gateway`, `METER`, `METER VALUE`) of the register(s) and parses the data accordingly.\n\nHowever, `mbusgemdecoder` package is only for data conversion. Use, for example, [pyModbusTCP](https://pypi.org/project/pyModbusTCP/) to obtain data to convert with `mbusgemdecoder`.\n',
    'author': 'René',
    'author_email': 'rene.pihlak@ttu.ee',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
