# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iac_test', 'iac_test.cli']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'RESTinstance>=1.3.0,<2.0.0',
 'click>=8.0.4,<9.0.0',
 'errorhandler>=2.0.1,<3.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'robotframework-jsonlibrary>=0.5,<0.6',
 'robotframework-pabot>=2.8.0,<3.0.0',
 'robotframework-requests>=0.9.4,<0.10.0',
 'robotframework>=6.0.1,<7.0.0',
 'ruamel-yaml>0.16.10']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=2.0.0,<3.0.0']}

entry_points = \
{'console_scripts': ['iac-test = iac_test.cli.main:main']}

setup_kwargs = {
    'name': 'iac-test',
    'version': '0.2.2',
    'description': 'A CLI tool to render and execute Robot Framework tests using Jinja templating.',
    'long_description': '[![Tests](https://github.com/netascode/iac-test/actions/workflows/test.yml/badge.svg)](https://github.com/netascode/iac-test/actions/workflows/test.yml)\n![Python Support](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-informational "Python Support: 3.7, 3.8, 3.9, 3.10, 3.11")\n\n# iac-test\n\nA CLI tool to render and execute [Robot Framework](https://robotframework.org/) tests using [Jinja](https://jinja.palletsprojects.com/) templating. Combining Robot\'s language agnostic syntax with the flexibility of Jinja templating allows dynamically rendering a set of test suites from the desired infrastructure state expressed in YAML syntax.\n\n```shell\n$ iac-test -h\nUsage: iac-test [OPTIONS]\n\n  A CLI tool to render and execute Robot Framework tests using Jinja\n  templating.\n\nOptions:\n  --version                  Show the version and exit.\n  -v, --verbosity LVL        Either CRITICAL, ERROR, WARNING, INFO or DEBUG\n  -d, --data PATH            Path to data YAML files. (env: IAC_TEST_DATA)\n                             [required]\n  -t, --templates DIRECTORY  Path to test templates. (env: IAC_TEST_TEMPLATES)\n                             [required]\n  -f, --filters DIRECTORY    Path to Jinja filters. (env: IAC_TEST_FILTERS)\n  --tests DIRECTORY          Path to Jinja tests. (env: IAC_TEST_TESTS)\n  -o, --output DIRECTORY     Path to output directory. (env: IAC_TEST_OUTPUT)\n                             [required]\n  -i, --include TEXT         Selects the test cases by tag (include). (env:\n                             IAC_TEST_INCLUDE)\n  -e, --exclude TEXT         Selects the test cases by tag (exclude). (env:\n                             IAC_TEST_EXCLUDE)\n  --render-only              Only render tests without executing them. (env:\n                             IAC_TEST_RENDER_ONLY)\n  -h, --help                 Show this message and exit.\n```\n\nAll data from the YAML files (`--data` option) will first be combined into a single data structure which is then provided as input to the templating process. Each template in the `--templates` path will then be rendered and written to the `--output` path. If the `--templates` path has subfolders, the folder structure will be retained when rendering the templates.\n\nAfter all templates have been rendered [Pabot](https://pabot.org/) will execute all test suites in parallel and create a test report in the `--output` path. The `--skiponfailure non-critical` argument will be used by default, meaning all failed tests with a `non-critical` tag will show up as "skipped" instead of "failed" in the final test report.\n\n## Installation\n\nPython 3.7+ is required to install `iac-test`. Don\'t have Python 3.7 or later? See [Python 3 Installation & Setup Guide](https://realpython.com/installing-python/).\n\n`iac-test` can be installed in a virtual environment using `pip`:\n\n```shell\npip install iac-test\n```\n\nThe following Robot libraries are installed with `iac-test`:\n\n- [RESTinstance](https://github.com/asyrjasalo/RESTinstance)\n- [Requests](https://github.com/MarketSquare/robotframework-requests)\n- [JSONLibrary](https://github.com/robotframework-thailand/robotframework-jsonlibrary)\n\nAny other libraries can of course be added via `pip`.\n\n## Ansible Vault Support\n\nValues in YAML files can be encrypted using [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html). This requires Ansible (`ansible-vault` command) to be installed and the following two environment variables to be defined:\n\n```\nexport ANSIBLE_VAULT_ID=dev\nexport ANSIBLE_VAULT_PASSWORD=Password123\n```\n\n`ANSIBLE_VAULT_ID` is optional, and if not defined will be omitted.\n\n## Additional Tags\n\n### Reading Environment Variables\n\nThe `!env` YAML tag can be used to read values from environment variables.\n\n```yaml\nroot:\n  name: !env VAR_NAME\n```\n\n## Example\n\n`data.yaml` located in `./data` folder:\n\n```yaml\n---\nroot:\n  children:\n    - name: ABC\n      param: value\n    - name: DEF\n      param: value\n```\n\n`test1.robot` located in `./templates` folder:\n\n```\n*** Settings ***\nDocumentation   Test1\n\n*** Test Cases ***\n{% for child in root.children | default([]) %}\n\nTest {{ child.name }}\n    Should Be Equal   {{ child.param }}   value\n{% endfor %}\n```\n\nAfter running `iac-test` with the following parameters:\n\n```shell\niac-test --data ./data --templates ./templates --output ./tests\n```\n\nThe following rendered Robot test suite can be found in the `./tests` folder:\n\n```\n*** Settings ***\nDocumentation   Test1\n\n*** Test Cases ***\n\nTest ABC\n    Should Be Equal   value   value\n\nTest DEF\n    Should Be Equal   value   value\n```\n\nAs well as the test results and reports:\n\n```shell\n$ tree -L 1 tests\ntests\n├── log.html\n├── output.xml\n├── pabot_results\n├── report.html\n├── test1.robot\n└── xunit.xml\n```\n\n## Custom Jinja Filters\n\nCustom Jinja filters can be used by providing a set of Python classes where each filter is implemented as a separate `Filter` class in a `.py` file located in the `--filters` path. The class must have a single attribute named `name`, the filter name, and a `classmethod()` named `filter` which has one or more arguments. A sample filter can be found below.\n\n```python\nclass Filter:\n    name = "filter1"\n\n    @classmethod\n    def filter(cls, data):\n        return str(data) + "_filtered"\n```\n\n## Custom Jinja Tests\n\nCustom Jinja tests can be used by providing a set of Python classes where each test is implemented as a separate `Test` class in a `.py` file located in the `--tests` path. The class must have a single attribute named `name`, the test name, and a `classmethod()` named `test` which has one or more arguments. A sample test can be found below.\n\n```python\nclass Test:\n    name = "test1"\n\n    @classmethod\n    def test(cls, data1, data2):\n        return data1 == data2\n```\n\n## Rendering Directives\n\nSpecial rendering directives exist to render a single test suite per (YAML) list item. The directive can be added to the Robot template as a Jinja comment following this syntax:\n\n```\n{# iterate_list <YAML_PATH_TO_LIST> <LIST_ITEM_ID> <JINJA_VARIABLE_NAME> #}\n```\n\nAfter running `iac-test` with the data from the previous [example](#example) and the following template:\n\n```\n{# iterate_list root.children name child_name #}\n*** Settings ***\nDocumentation   Test1\n\n*** Test Cases ***\n{% for child in root.children | default([]) %}\n{% if child.name == child_name %}\n\nTest {{ child.name }}\n    Should Be Equal   {{ child.param }}   value\n{% endif %}\n{% endfor %}\n```\n\nThe following test suites will be rendered:\n\n```shell\n$ tree -L 2 tests\ntests\n├── ABC\n│   └── test1.robot\n└── DEF\n    └── test1.robot\n```\n\nA similar directive exists to put the test suites in a common folder though with a unique filename.\n\n```\n{# iterate_list_folder <YAML_PATH_TO_LIST> <LIST_ITEM_ID> <JINJA_VARIABLE_NAME> #}\n```\n\nThe following test suites will be rendered:\n\n```shell\n$ tree -L 2 tests\ntests\n└── test1\n    ├── ABC.robot\n    └── DEF.robot\n```\n\n## Select Test Cases By Tag\n\nIt is possible to include and exclude test cases by tag names with the `--include` and `--exclude` CLI options. These options are directly passed to the Pabot/Robot executor and are documented [here](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#by-tag-names).\n',
    'author': 'Daniel Schmidt',
    'author_email': 'danischm@cisco.com',
    'maintainer': 'Daniel Schmidt',
    'maintainer_email': 'danischm@cisco.com',
    'url': 'https://github.com/netascode/iac-test',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
