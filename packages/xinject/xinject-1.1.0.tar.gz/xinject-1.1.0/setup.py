# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xinject', 'xinject._private']

package_data = \
{'': ['*']}

install_requires = \
['xsentinels>=1.2.0,<2.0.0']

entry_points = \
{'pytest11': ['xinject_pytest_plugin = xinject.pytest_plugin']}

setup_kwargs = {
    'name': 'xinject',
    'version': '1.1.0',
    'description': 'Lazy dependency injection.',
    'long_description': '![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.8|%203.9|%203.10&color=blue?style=flat-square&logo=python)\n![PyPI version](https://badge.fury.io/py/xinject.svg?)\n\n- [Introduction](#introduction)\n- [Documentation](#documentation)\n- [Install](#install)\n- [Quick Start](#quick-start)\n- [Licensing](#licensing)\n\n# Introduction\n\nMain focus is an easy way to create lazy universally injectable dependencies;\nin less magical way. It also leans more on the side of making it easier to get\nthe dependency you need anywhere in the codebase.\n\npy-xinject allows you to easily inject lazily created universal dependencies into whatever code that needs them,\nin an easy to understand and self-documenting way.\n\n# Documentation\n\n**[📄 Detailed Documentation](https://xyngular.github.io/py-xinject/latest/)** | **[🐍 PyPi](https://pypi.org/project/xinject/)**\n\n# Install\n\n```bash\n# via pip\npip install xinject\n\n# via poetry\npoetry add xinject\n```\n\n# Quick Start\n\n```python\n# This is the "my_resources.py" file/module.\n\nimport boto3\nfrom xinject import DependencyPerThread\n\n\nclass S3(DependencyPerThread):\n    def __init__(self, **kwargs):\n        # Keeping this simple; a more complex version\n        # may store the `kwargs` and lazily create the s3 resource\n        # only when it\'s asked for (via a `@property or some such).\n\n        self.resource = boto3.resource(\'s3\', **kwargs)\n```\n\nTo use this resource in codebase, you can do this:\n\n```python\n# This is the "my_functions.py" file/module\n\nfrom .my_resources import S3\n\ndef download_file(file_name, dest_path):\n    # Get dependency\n    s3_resource = S3.grab().resource\n    s3_resource.Bucket(\'my-bucket\').download_file(file_name, dest_path)\n```\n\nInject a different version of the resource:\n\n```python\nfrom .my_resources import S3\nfrom .my_functions import download_file\n\nus_west_s3_resource = S3(region_name=\'us-west-2\')\n\ndef get_s3_file_from_us_west(file, dest_path):\n    # Can use Dependencies as a context-manager,\n    # inject `use_west_s3_resource` inside `with`:\n    with us_west_s3_resource:\n        download_file(file, dest_path)\n\n# Can also use Dependencies as a function decorator,\n# inject `use_west_s3_resource` whenever this method is called.\n@us_west_s3_resource\ndef get_s3_file_from_us_west(file, dest_path):\n    download_file(file, dest_path)\n```\n\n# Licensing\n\nThis library is licensed under the MIT-0 License. See the LICENSE file.\n',
    'author': 'Josh Orr',
    'author_email': 'josh@orr.blue',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xyngular/py-xinject',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
