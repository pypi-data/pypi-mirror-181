# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt', 'dbt.adapters.ibmdb2', 'dbt.include.ibmdb2']

package_data = \
{'': ['*'],
 'dbt.include.ibmdb2': ['macros/*',
                        'macros/materializations/incremental/*',
                        'macros/materializations/table/*',
                        'macros/materializations/view/*',
                        'macros/utils/*']}

install_requires = \
['dbt-core>=1.0.0,<2.0.0', 'ibm-db>=3.1.0,<4.0.0']

setup_kwargs = {
    'name': 'dbt-ibmdb2',
    'version': '0.4.3',
    'description': 'The db2 adapter plugin for dbt (data build tool)',
    'long_description': '[![pypi](https://badge.fury.io/py/dbt-ibmdb2.svg)](https://pypi.org/project/dbt-ibmdb2/)\n[![python](https://img.shields.io/pypi/pyversions/dbt-ibmdb2)](https://pypi.org/project/dbt-ibmdb2/)\n\n# dbt-ibmdb2\n\nThis plugin ports [dbt](https://getdbt.com) functionality to IBM DB2.\n\nThis is an experimental plugin:\n- We have not tested it extensively\n- Only basic tests are implemented\n- Compatibility with other [dbt packages](https://hub.getdbt.com/) (like [dbt_utils](https://hub.getdbt.com/fishtown-analytics/dbt_utils/latest/)) is only partially tested\n\nPlease read these docs carefully and use at your own risk. [Issues](https://github.com/aurany/dbt-ibmdb2/issues/new) welcome!\n\nTable of Contents\n=================\n\n   * [Installation](#installation)\n   * [Supported features](#supported-features)\n   * [Configuring your profile](#configuring-your-profile)\n   * [Running Tests](#setup-dev-environment-and-run-tests)\n   * [Reporting bugs](#reporting-bugs)\n\n### Installation\nThis plugin can be installed via pip:\n\n```bash\n$ pip install dbt-ibmdb2\n```\n\n### Supported features\n\n| DB2 LUW | DB2 z/OS | Feature |\n|:---------:|:---:|---------------------|\n| ✅ | 🤷 | Table materialization       |\n| ✅ | 🤷 | View materialization        |\n| ✅ | 🤷 | Incremental materialization |\n| ✅ | 🤷 | Ephemeral materialization   |\n| ✅ | 🤷 | Seeds                       |\n| ✅ | 🤷 | Sources                     |\n| ✅ | 🤷 | Custom data tests           |\n| ✅ | 🤷 | Docs generate               |\n| ✅ | 🤷 | Snapshots                   |\n\n*Notes:*\n- dbt-ibmdb2 is built on the ibm_db python package and there are some known encoding issues related to z/OS.\n\n### Configuring your profile\n\nA dbt profile can be configured to run against DB2 using the following configuration example:\n\n**Example entry for profiles.yml:**\n\n```\nyour_profile_name:\n  target: dev\n  outputs:\n    dev:\n      type: ibmdb2\n      schema: analytics\n      database: test\n      host: localhost\n      port: 50000\n      protocol: TCPIP\n      username: my_username\n      password: my_password\n      extra_connect_opts: my_extra_config_options\n```\n\n| Option          | Description                                                                         | Required?                                                          | Example                                        |\n| --------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------- |\n| type            | The specific adapter to use                                                         | Required                                                           | `ibmdb2`                                       |\n| schema          | Specify the schema (database) to build models into                                  | Required                                                           | `analytics`                                    |\n| database        | Specify the database you want to connect to                                         | Required                                                           | `testdb`                                         |\n| host            | Hostname or IP-adress                                                               | Required                                                           | `localhost`                                    |\n| port            | The port to use                                                                     | Optional                                                           | `50000`                                        |\n| protocol        | Protocol to use                                                                     | Optional                                                           | `TCPIP`                                        |\n| username        | The username to use to connect to the server                                        | Required                                                           | `my-username`                                  |\n| password        | The password to use for authenticating to the server                                | Required                                                           | `my-password`                                  |\n| extra_connect_opts        | Extra connection options                                | Optional                                                           | `Security=SSL;SSLClientKeyStoreDB=<path-to-client-keystore>;SSLClientKeyStash=<path-to-client-keystash>`                                  |\n\n### Setup dev environment and run tests\n\nMake sure you have docker and poetry installed globally.\n\n```\nmake install\nmake test\nmake uninstall\n```\n\n### Reporting bugs\n\nWant to report a bug or request a feature? Open [an issue](https://github.com/aurany/dbt-ibmdb2/issues/new).\n\n### Credits\n\ndbt-ibmdb2 is heavily inspired by and borrows from [dbt-mysql](https://github.com/dbeatty10/dbt-mysql) and [dbt-oracle](https://github.com/techindicium/dbt-oracle).\n',
    'author': 'aurany',
    'author_email': 'rasmus.nyberg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aurany/dbt-ibmdb2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2',
}


setup(**setup_kwargs)
