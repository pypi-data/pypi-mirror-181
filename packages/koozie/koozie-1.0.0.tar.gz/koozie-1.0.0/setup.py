# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koozie']

package_data = \
{'': ['*']}

install_requires = \
['pint>=0.18,<0.19']

setup_kwargs = {
    'name': 'koozie',
    'version': '1.0.0',
    'description': 'A light-weight wrapper around pint.',
    'long_description': "[![Release](https://img.shields.io/pypi/v/koozie.svg)](https://pypi.python.org/pypi/koozie)\n\n[![Test](https://github.com/bigladder/koozie/actions/workflows/test.yaml/badge.svg)](https://github.com/bigladder/koozie/actions/workflows/test.yaml)\n\nkoozie\n======\n\n*koozie* is a light-weight wrapper around [*pint*](https://pint.readthedocs.io/en/stable/). The intent is to provide much of the functionality without worrying about the setup. It uses quantities internally, but its functions only return floats. This approach reflects the opinion that all calculations should be performed in Standard base SI units, and any conversions can happen via pre- or post-processing for usability. This minimizes additional operations in performance critical code.\n\n*koozie* also defines a few convenient aliases for different units. See the [source code](https://github.com/bigladder/koozie/blob/master/koozie/koozie.py) for details. A list of other available units is defined in [pint's default units definition file](https://github.com/hgrecco/pint/blob/master/pint/default_en.txt).\n\nThere are three public functions in *koozie*:\n\n- `fr_u(value, from_units)`: Convert a value from given units to base SI units\n- `to_u(value, to_units)`: Convert a value from base SI units to given units\n- `convert(value, from_units, to_units)`: Convert from any units to another units of the same dimension\n\nExample usage can be found in the [test file](https://github.com/bigladder/koozie/blob/master/test/test_koozie.py).\n",
    'author': 'Big Ladder Software',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bigladder/koozie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
