# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datek_app_utils', 'datek_app_utils.env_config']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datek-app-utils',
    'version': '0.3.5',
    'description': 'Utilities for building applications',
    'long_description': '[![codecov](https://codecov.io/gh/DAtek/datek-app-utils/branch/master/graph/badge.svg?token=UR0G0I41LD)](https://codecov.io/gh/DAtek/datek-app-utils)\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>\n\n# Utilities for building applications.\n\n## Contains:\n- Config loading from environment\n- Bootstrap for logging\n- Base class for creating async workers\n- Async timeout decorator, which is very useful for writing async tests\n\n## Examples:\n\n### Env config\n```python\nimport os\n\nfrom datek_app_utils.env_config.base import BaseConfig\n\nos.environ["COLOR"] = "RED"\nos.environ["TEMPERATURE"] = "50"\n\n\nclass Config(BaseConfig):\n    COLOR: str\n    TEMPERATURE: int\n\n\nassert Config.COLOR == "RED"\nassert Config.TEMPERATURE == 50\n```\n\nThe `Config` class casts the values automatically.\nMoreover, you can test whether all the mandatory variables have been set or not.\n\n```python\nimport os\n\nfrom datek_app_utils.env_config.base import BaseConfig\nfrom datek_app_utils.env_config.utils import validate_config\nfrom datek_app_utils.env_config.errors import ValidationError\n\nos.environ["COLOR"] = "RED"\n\n\nclass Config(BaseConfig):\n    COLOR: str\n    TEMPERATURE: int\n    AMOUNT: int = None\n\n\ntry:\n    validate_config(Config)\nexcept ValidationError as error:\n    for attribute_error in error.errors:\n        print(attribute_error)\n\n```\nOutput:\n```\nTEMPERATURE: Not set. Required type: <class \'int\'>\n```\n\n### Async timeout decorator\n\n```python\nfrom asyncio import sleep, run\nfrom datek_app_utils.async_utils import async_timeout\n\n\n@async_timeout(0.1)\nasync def sleep_one_sec():\n    await sleep(1)\n\n    \nrun(sleep_one_sec())\n\n```\nOutput:\n```\nTimeoutError\n```\n',
    'author': 'Attila Dudas',
    'author_email': 'dudasa7@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DAtek/datek-app-utils/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
