# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qorus_remote', 'qorus_remote.tools']

package_data = \
{'': ['*'], 'qorus_remote.tools': ['templates/*']}

install_requires = \
['pyaml', 'requests', 'urllib3', 'websocket-client']

entry_points = \
{'console_scripts': ['make-release = qorus_remote.tools.make_release:main',
                     'qorus-remote-commands = '
                     'qorus_remote.tools.qorus_remote_commands:main']}

setup_kwargs = {
    'name': 'qorus-remote',
    'version': '1.0.2',
    'description': 'A package with scripts for use with remote Qorus instances',
    'long_description': "# Overview\n\nThis package contains two scripts:\n- `qorus-remote-commands`: allows for command-line access to a remote Qorus server\n- `make-release`: allows for releases to be created from local files\n\n# Remote Qorus Commands\nRequires Qorus 5.0.4+ and Python 3\n\nThe `qorus-remote-commands` script allows the user to run Qorus and Qore commands on a remote Qorus server using the\nQorus HTTP server and receive the output of the executed command in real time via the WebSocket protocol.\n\nThis allows the Qorus client to be used on any system with python 3 and to access Qorus running in a container or in\nany other type of deployment as long as the HTTP server is accessible.\n\n**NOTE**: the `oload` command is mean to be used with local files; local files are copied to the server to a temporary\nlocation, and then `oload` is executed on the server with the deployed files.  At the end of the remote `oload`\nexecution, the temporary files are deleted,\n\n## Installation\n\nInstall via pip:\n\n`pip install qorus-remote`\n\n## Usage\n`qorus-remote-commands [-h|--help|--usage] <NETRC-FILE> <COMMAND> [<COMMAND-ARGS> ...]`\n\n## Concrete Usage Examples\n\n`qorus-remote-commands ~/.netrc-qorus-local qctl ps`\n\n`qorus-remote-commands ~/.netrc-qorus-local qctl threads qorus-core`\n\n`qorus-remote-commands ~/.netrc-qorus-local qrest system/starttime`\n\n## .netrc file\n| Variable | Description | Mandatory |\n| --- | --- | --- |\n| `machine` | ip address of the Qorus server machine | Yes |\n| `port` | port of the Qorus server machine | Yes |\n| `secure` | `yes` if the Qorus server is on `https`, no otherwise | Yes |\n| `login` | Qorus username | Yes |\n| `password` | Qorus password | Yes |\n| `timeout` | Maximum time in seconds allowed for each of the curl operation | No |\n| `verbose` | Makes the script verbose | No |\n| `nodelete` | Does not delete the upload folder on the server | No |\n\n### Example .netrc file\nFor a Qorus server located on https://localhost:8011 and using the Qorus user `adm` (`.netrc-qorus-local`):\n```\nmachine localhost\nport 8011\nsecure yes\nlogin adm\npassword adm\ntimeout 120\nverbose no\n```\n\n## Commands\n\n### Qorus commands\n`oload`\\\n`ocmd`\\\n`ojview`\\\n`oprop`\\\n`ostart`\\\n`ostatus`\\\n`ostop`\\\n`oview`\\\n`make-release`\\\n`qctl`\\\n`qrest`\\\n`schema-tool`\\\n`user-tool`\n\n### Qore commands\n`rest`\\\n`schema-reverse`\\\n`sfrest`\\\n`soaputil`\\\n`sqlutil`\\\n`qdp`\\\n`saprest`\n\n### Aliases\n\nIt's recommended to create aliases for each of the above commands like:\n- Unix/Linux: `alias oload='qorus-remote-commands ~/.netrc-qorus-local oload $*'`\n- Windows: `DOSKEY oload=qorus-remote-commands %USERPROFILE%\\Qorus\\netrc-qorus-local oload $*`\n\netc\n\n# make-release\n\nThe `make-release` script allows the user to make Qorus releases that can be manually or automatically deployed to\nQorus servers.\n\n## Examples\n`make-release -U. mylabel services/*.qsd`\n\nCreates a user-code release with all service files in the default release-dir/mylabel directory.\n\n`make-release -U. -lmylabel services/*.qsd`\n\nCeates only the load script manifest for service files in a release named mylabel.qrf\n",
    'author': 'Qore Technologies, s.r.o.',
    'author_email': 'info@qoretechnologies.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://qoretechnologies.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
