# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ko_poetry_audit_plugin']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.23.0,<0.24.0',
 'poetry>=1.2.2,<2.0.0',
 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'poetry.application.plugin': ['demo = '
                               'ko_poetry_audit_plugin.plugins:AuditApplicationPlugin']}

setup_kwargs = {
    'name': 'ko-poetry-audit-plugin',
    'version': '0.7.0',
    'description': 'Poetry plugin to check known vulnerabilities from poetry.lock',
    'long_description': "# ko-poetry-audit-plugin\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![formatter](https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg)](https://github.com/PyCQA/docformatter)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)\n\nTo check known vulnerabilities from `poetry.lock`.\n\nInspired by [pypa/pip-audit](https://github.com/pypa/pip-audit), this adds `audit` command tip [`poetry`](https://python-poetry.org/docs/), for checking vulnerabilities of packages found in `poetry.lock`.\n\nVulnerability reports are sourced from Python Packaging Advisory Database (https://github.com/pypa/advisory-database) using [JSON API](https://warehouse.pypa.io/api-reference/json.html).\n\n## Installation\n\nPlease follow poetry [Using Plugins](https://python-poetry.org/docs/plugins/#using-plugins) for installation.\n```\n% poetry self add ko-poetry-audit-plugin\n```\n\nTo integrate with [`pre-commit`](https://pre-commit.com), trigger scan whenever `poetry.lock` is commit:\n```yaml\n  - repo: https://github.com/koyeung/ko-poetry-audit-plugin.git\n    rev: 0.6.0\n    hooks:\n      - id: poetry-audit\n```\n\n**Note** by default, it scans for `main` and `dev` dependencies groups only.\n\n\n## Usage\n\nTo check for `main` group:\n\n```\n% poetry audit\nNo known vulnerabilities found\n```\n\nTo include packages in `dev` group:\n```\n% poetry audit --with dev\nFound vulnerabilities\nGroup    Name    Version    ID                   Withdrawn    Fix Versions    Link\n-------  ------  ---------  -------------------  -----------  --------------  -------------------------------------------------\ndev      py      1.11.0     GHSA-w596-4wvx-j9j6                               https://osv.dev/vulnerability/GHSA-w596-4wvx-j9j6\ndev      py      1.11.0     PYSEC-2022-42969                                  https://osv.dev/vulnerability/PYSEC-2022-42969\n% echo $?\n1\n```\n\nTo show more details:\n```\n% poetry audit --with dev -vv\n[ko_poetry_audit_plugin.auditor] get packages list from dependencies groups={'main', 'dev'}\n[ko_poetry_audit_plugin.pypi_warehouse] package.name='boto3', package.version='1.26.8': no vulnerabilities found\n[ko_poetry_audit_plugin.pypi_warehouse] package.name='jmespath', package.version='1.0.1': no vulnerabilities found\n[ko_poetry_audit_plugin.pypi_warehouse] package.name='botocore', package.version='1.29.8': no vulnerabilities found\n[ko_poetry_audit_plugin.pypi_warehouse] package.name='six', package.version='1.16.0': no vulnerabilities found\n[ko_poetry_audit_plugin.pypi_warehouse] package.name='python-dateutil', package.version='2.8.2': no vulnerabilities found\n[ko_poetry_audit_plugin.pypi_warehouse] package.name='s3transfer', package.version='0.6.0': no vulnerabilities found\n[ko_poetry_audit_plugin.pypi_warehouse] package.name='py', package.version='1.11.0': vulnerabilities found\n[ko_poetry_audit_plugin.pypi_warehouse] package.name='urllib3', package.version='1.26.12': no vulnerabilities found\nFound vulnerabilities\nGroup    Name    Version    ID                   Withdrawn    Fix Versions    Link\n-------  ------  ---------  -------------------  -----------  --------------  -------------------------------------------------\ndev      py      1.11.0     GHSA-w596-4wvx-j9j6                               https://osv.dev/vulnerability/GHSA-w596-4wvx-j9j6\ndev      py      1.11.0     PYSEC-2022-42969                                  https://osv.dev/vulnerability/PYSEC-2022-42969\n```\n\n## Exit codes\n`poetry audit` exits with non-zero code, unless all vulnerabilities found have been withdrawn.\n\n**Note** only packages found on `pypi` could be checked.\n\n## Licensing\n`poetry audit` plugin is licensed under the Apache 2.0 License.\n",
    'author': 'YEUNG King On',
    'author_email': 'koyeung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
