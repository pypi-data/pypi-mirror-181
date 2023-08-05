# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['prefect_yaml']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'prefect>=2.7.1,<3.0.0', 'ruamel-yaml>=0.17.21,<0.18.0']

extras_require = \
{'docs': ['Sphinx>=5.0,<6.0',
          'insipid-sphinx-theme>=0.3.6,<0.4.0',
          'myst-parser>=0.18,<0.19']}

entry_points = \
{'console_scripts': ['prefect-yaml = prefect_yaml.cli:main']}

setup_kwargs = {
    'name': 'prefect-yaml',
    'version': '2022.1.0',
    'description': 'Prefect scheduler for YAML configuration',
    'long_description': '# Prefect YAML\n\n<p align="center">\n  <a href="https://github.com/factorpricingmodel/prefect-yaml/actions?query=workflow%3ACI">\n    <img src="https://img.shields.io/github/workflow/status/factorpricingmodel/prefect-yaml/CI/main?label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://prefect-yaml.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/prefect-yaml.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/factorpricingmodel/prefect-yaml">\n    <img src="https://img.shields.io/codecov/c/github/factorpricingmodel/prefect-yaml.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/prefect-yaml/">\n    <img src="https://img.shields.io/pypi/v/prefect-yaml.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/prefect-yaml.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/prefect-yaml.svg?style=flat-square" alt="License">\n</p>\n\nPackage to run prefect with YAML configuration. For further details, please refer\nto the [documentation](https://prefect-yaml.readthedocs.io/en/latest/)\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install prefect-yaml`\n\n## Usage\n\nRun the command line `prefect-yaml` with the specified configuration\nfile.\n\nFor example, the following YAML configuration is located in [examples/simple_config.yaml](examples/simple_config.yaml).\n\n```\nmetadata:\n  output-directory: .output\n\ntask:\n  task_a:\n    caller: math:fabs\n    parameters:\n      - -9.0\n    output:\n      format: json\n  task_b:\n    caller: math:sqrt\n    parameters:\n      - !data task_a\n```\n\nRun the following command to generate all the task outputs to the\ndirectory `.output` in the running directory.\n\n```shell\nprefect-yaml -c examples/simple_config.yaml\n```\n\nThe output directory contains all the task outputs in the specified\nformat. The default format is pickle.\n\n```shell\n% tree .output\n.output\n├── task_a.json\n└── task_b.pickle\n\n0 directories, 2 files\n```\n\n## Configuration\n\nEach configuration must specify the section of `metadata` and `task`.\n\n### Metadata\n\nMetadata section contains the following parameters.\n\n|     Parameter      |         Description         | Required / Optional |\n| :----------------: | :-------------------------: | :-----------------: |\n| `output-directory` | Filesystem output directory |      Required       |\n\n### Task\n\nEach task is a key-value pair where the key is the name of the task,\nand the value is a dictionary of parameters.\n\n|  Parameter   | Subsection |                                        Description                                        | Required / Optional |\n| :----------: | :--------: | :---------------------------------------------------------------------------------------: | :-----------------: |\n|   `caller`   |            |          Caller module and function name. In the format of `<module>:<function>`          |      Required       |\n| `parameters` |            | Function arguments. Either a list of unnamed arguments or a dictionary of named arguments |     (Optional)      |\n|   `format`   |  `output`  |   Output format. Supported stdlib formats are `pickle` and `json`. Default is `pickle`.   |     (Optional)      |\n|    `name`    |  `output`  |                Name of the output file. Default is same as the task name.                 |     (Optional)      |\n',
    'author': 'Factor Pricing Model',
    'author_email': 'factor.pricing.model@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/factorpricingmodel/prefect-yaml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
