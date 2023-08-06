# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uai_uri_interface']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'uai-uri-interface',
    'version': '0.1.6',
    'description': '',
    'long_description': '# URI Inteface\n\nThis package provides an interface for file access that is basically a subset of pathlib.Path. It is needed because we internally use a path abstraction that allows for exactly this subset of operations. So for debugging methods that take an URI as input you can put in a pathlib.Path while we internally will input our path abstraction.\n',
    'author': 'understand.ai',
    'author_email': 'postmaster@understand.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
