# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splunk_contentctl',
 'splunk_contentctl.actions',
 'splunk_contentctl.actions.detection_testing',
 'splunk_contentctl.actions.detection_testing.modules',
 'splunk_contentctl.enrichments',
 'splunk_contentctl.helper',
 'splunk_contentctl.input',
 'splunk_contentctl.objects',
 'splunk_contentctl.output']

package_data = \
{'': ['*'],
 'splunk_contentctl': ['templates/*',
                       'templates/detections/*',
                       'templates/macros/*',
                       'templates/splunk_app/metadata/*',
                       'templates/stories/*',
                       'templates/tests/*'],
 'splunk_contentctl.output': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'attackcti>=0.3.7,<0.4.0',
 'docker>=6.0.1,<7.0.0',
 'gitpython>=3.1.29,<4.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pycvesearch>=1.2,<2.0',
 'pydantic>=1.10.2,<2.0.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'semantic-version>=2.10.0,<3.0.0',
 'splunk-sdk>=1.7.2,<2.0.0',
 'validators>=0.20.0,<0.21.0',
 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['contentctl = splunk_contentctl.contentctl:main']}

setup_kwargs = {
    'name': 'splunk-contentctl',
    'version': '1.0.3',
    'description': 'Splunk Content Control Tool',
    'long_description': '\n# Splunk Contentctl\n![logo](docs/contentctl-logo.png)\n=====\n\n\n\n## Installation\nInstall contentctl using pip. Make sure you use python version 3.9:\n```\npip install \n```\n\n\n## Usage\n\n1. **init** - Initilialize a new repo from scratch so you can easily add your own content to a custom application. \n2. **new** - Creates new content (detection, story)\n3. **validate** - Validates written content\n4. **build** - Builds an application suitable for deployment on a search head using Slim, the Splunk Packaging Toolkit\n5. **deploy** - Deploy the security content pack to a Splunk Server\n6. **docs** - Create documentation as Markdown\n7. **reporting** - Create different reporting files such as a Mitre ATT&CK overlay\n\n\n',
    'author': 'STRT',
    'author_email': 'research@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
