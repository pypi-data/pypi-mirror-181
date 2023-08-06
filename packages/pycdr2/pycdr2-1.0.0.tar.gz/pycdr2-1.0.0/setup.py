# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycdr2',
 'pycdr2._typesupport',
 'pycdr2._typesupport.DDS',
 'pycdr2._typesupport.DDS.XTypes']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.9"': ['typing-extensions>=4.4.0']}

setup_kwargs = {
    'name': 'pycdr2',
    'version': '1.0.0',
    'description': 'The IDL part of the CycloneDDS package as standalone version, to support packages that need CDR (de)serialisation without the Cyclone DDS API.',
    'long_description': '# PyCDR2\n\nPyCDR2 is the standalone version of `cyclonedds.idl`. The documentation of [cyclonedds.io/docs/cyclonedds-python/latest/idl.html](https://cyclonedds.io/docs/cyclonedds-python/latest/idl.html) still applies, you just have to replace `cyclonedds.idl` with `pycdr2`.\n',
    'author': 'Thijs Miedema',
    'author_email': 'opensource@tmiedema.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
