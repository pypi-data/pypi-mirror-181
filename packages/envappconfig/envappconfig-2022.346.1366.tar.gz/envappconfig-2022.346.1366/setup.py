# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envappconfig']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'envappconfig',
    'version': '2022.346.1366',
    'description': 'Simple app configuration via environment variables, in the spirit of argparse.',
    'long_description': "# envappconfig\n\nenvappconfig is intended to provide simple configuration via environment variables, in the same spirit as argparse.\n\nFeatures:\n* Autogenerates usage output if an environment variable is missing\n* Default settings for missing environment variables\n* Functions that transform the environment variable string to the value you need\n* Environment variable prefixes\n* Optional dictionary of the config\n\n## Basic example\n\n```python\nfrom envappconfig import EnvAppConfig\n\nconfig = EnvAppConfig(description='Amazing app')\nconfig.add_env('port', default=1234, transform=int, help='The listen port')\nconfig.add_env('mirror', help='The URL to mirror')\nconfig.configure()\n\n# Returns PORT from os.environ transformed to an int,\n# or 1234 if PORT does not exist.\nconfig.port\n\n# Returns MIRROR from os.environ,\n# or displays usage if MIRROR does not exist, then exits.\nconfig.mirror\n```\n\n## Adding a prefix\n\nIf all the environment variables for the app have the same prefix, it can be specified with the `prefix` parameter.\n\n```python\nfrom envappconfig import EnvAppConfig\n\nconfig = EnvAppConfig(prefix='MYAPP', description='Amazing app')\nconfig.add_env('port', default=1234, transform=int, help='The listen port')\nconfig.add_env('mirror', help='The URL to mirror')\nconfig.configure()\n\n# Returns MYAPP_PORT from os.environ transformed to an int,\n# or 1234 if MYAPP_PORT does not exist.\nconfig.port\n\n# Returns MYAPP_MIRROR from os.environ,\n# or displays usage if MYAPP_MIRROR does not exist, then exits.\nconfig.mirror\n```\n\n## Custom transforms\n\nThe `transform` parameter can be used to specify normal transforms, like `int` or `float` (the default is `str`), but it can also take custom transform functions.  The transform function must take a single parameter, which will be filled in with the string value from the environment variable.\n\n```python\nconfig = EnvAppConfig(prefix='MYAPP', description='Amazing app')\n\n# Double the timeout specified in the TIMEOUT environment variable,\n# or default to 60.\nconfig.add_env('timeout', default=60, transform=lambda x: int(x) * 2, help='Timeout in seconds')\n...\n```\n\n## Adding more config values\n\nAdditional config values can be added to an existing EnvAppConfig, which can be helpful when there's a config value that needs to be calculated based on other config values.\n\n```python\nfrom envappconfig import EnvAppConfig\n\nconfig = EnvAppConfig(description='Amazing app')\nconfig.add_env('bind', help='IP address to bind to')\nconfig.add_env('port', default=1234, transform=int, help='The listen port')\nconfig.configure()\nconfig.add_conf('listen', f'{config.bind}:{config.port}')\n\n# Returns the combined bind:port string.\nconfig.listen\n```\n\n## Getting a config dictionary\n\nThe EnvAppConfig instance is also available as a dictionary.\n\n```python\nfrom envappconfig import EnvAppConfig\n\nconfig = EnvAppConfig(description='Amazing app')\nconfig.add_env('bind', help='IP address to bind to')\nconfig.add_env('port', default=1234, transform=int, help='The listen port')\nconfig.configure()\n\n# Returns a dictionary containing {'bind': '1.2.3.4', 'port': 1234}\nconfig.asdict()\n```\n",
    'author': 'Spectric Labs',
    'author_email': 'foss@spectric.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/spectriclabs/envappconfig',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
