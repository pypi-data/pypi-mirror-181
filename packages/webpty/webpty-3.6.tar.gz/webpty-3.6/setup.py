# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webpty']

package_data = \
{'': ['*'], 'webpty': ['static/*']}

install_requires = \
['importlib-metadata>=5.1.0,<6.0.0', 'requests==2.28.1', 'tornado==6.2']

setup_kwargs = {
    'name': 'webpty',
    'version': '3.6',
    'description': 'A web-based application to access shell & shell based applications via a browser',
    'long_description': '# webpty\n\nWeb based application to access shell & shell based applications via a browser.\n\n[![PyPI version](https://badge.fury.io/py/webpty.svg)](https://badge.fury.io/py/webpty)\n\n#\n\n## Installation\n\nUse [pip](https://pip.pypa.io/en/stable/) and install webpty.\n\n```bash\npip install webpty\n```\n\n## Usage\n\n```bash\nwebpty\n```\n\nCreates a tornado server which will be serving bash shell on http://localhost:8000/\n\n### Change Shell\n\n```bash\nwebpty -c $SHELL\n```\n\nor\n\n```bash\nwebpty --cmd=$SHELL\n\n```\n\nThis $SHELL can be bash, sh, python, vim, wtfutil, etc. that is available in the system.\n\n### Change Port\n\n```bash\nwebpty -p $PORT\n```\n\nor\n\n```bash\nwebpty --port=$PORT\n\n```\n\nCreates a tornado server that server on the specified port http://localhost:$PORT/\n\n### Change Allowed Hosts\n\nBy default, server will accept request from all the hosts without any restriction, to make it accept only from certain hosts,\n\n```bash\nwebpty -ah $ALLOWED_HOSTS\n```\n\nor\n\n```bash\nwebpty --allowed-hosts=$ALLOWED_HOSTS\n```\n\nServer accepts only requests from $ALLOWED_HOSTS. This $ALLOWED_HOSTS should be list of strings seperated by a comma.\n\n#\n\n## Screenshots\n\n#### Bash\n\n![Online Bash Shell](https://imgur.com/iNoW3jL.png)\n\n#### Python\n\n![Online Python Shell](https://imgur.com/YYK4YXs.png)\n\n#### Vim\n\n![Online Vim](https://imgur.com/vfei1Ri.png)\n\n#\n\n## Contributing\n\nPull requests are welcome. Raise a issue and start a discussion before submitting a pr.\n\n#\n\n![Python Powered](https://www.python.org/static/community_logos/python-powered-h-70x91.png)\n',
    'author': 'Satheesh Kumar',
    'author_email': 'mail@satheesh.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
