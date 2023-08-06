# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssh_assets',
 'ssh_assets.authorized_keys',
 'ssh_assets.bin',
 'ssh_assets.bin.ssh_assets',
 'ssh_assets.bin.ssh_assets.groups',
 'ssh_assets.bin.ssh_assets.keys',
 'ssh_assets.configuration',
 'ssh_assets.keys',
 'ssh_assets.token']

package_data = \
{'': ['*']}

install_requires = \
['cli-toolkit>=2.2,<3.0']

entry_points = \
{'console_scripts': ['ssh-assets = ssh_assets.bin.ssh_assets.main:main']}

setup_kwargs = {
    'name': 'ssh-assets',
    'version': '1.6.6',
    'description': 'SSH asset and key management tools',
    'long_description': '![Unit Tests](https://github.com/hile/ssh-assets/actions/workflows/unittest.yml/badge.svg)\n![Style Checks](https://github.com/hile/ssh-assets/actions/workflows/lint.yml/badge.svg)\n\n# SSH assets python library\n\nThis little utility allows configuring SSH keys to be loaded automatically to\nthe SSH agent based on asset configuration files, and can detect loaded keys\nbased on the key hash to avoid reloading existing keys.\n\nThis library can:\n\n- load SSH key details from various key formats to get key hashes, comments and other key details\n- detect keys loaded to the SSH agent by key hash instead of filename\n- define known SSH keys from multiple locations (project specific folders, shared team folders) with\n  options to name and autoload the key with the module\n- load and unload keys to the agent based on custom configuration file, without asking key password\n  if the key was already loaded\n\n# Installing\n\nThis tool can be installed from PyPI.\n\n```bash\npip install ssh-assets\n```\n\n## Using the CLI tool\n\nThis package installs command line utility `ssh-assets`. The tool currently has\nonly one command `load-keys` that can be used to load the keys configured in\nthe assets configuration file as shown below.\n\nFollowing command loads any keys not yet loaded to the agent, but limits this\nto the keys with `autoload` property set to `true`:\n\n```bash\nssh-assets keys load\nssh-assets keys load --group personal\nssh-assets keys edit personal --no-autoload\nssh-assets keys edit personal --autoload\nssh-assets keys add demo --path ~/.ssh/id_rsa.demo --autoload --expire=8h\nssh-assets keys delete demo\n```\n\n## SSH assets configuration file\n\nThis module uses configuration file `~/.ssh/assets.yml` to define paths to the\nSSH keys.\n\nExample configuration file:\n\n```yaml\n---\ngroups:\n  - name: personal\n    expire: 5d\n    keys:\n      - personal\n      - missing-demo-key\n  - name: work\n    expire: 1d\n    keys:\n      - aws\n      - master\n      - myproject\nkeys:\n  - name: personal\n    path: ~/.ssh/id_rsa\n    autoload: true\n  - name: aws\n    path: ~/.ssh/id_rsa-aws\n  - name: myproject\n    path: ~/Work/Keys/ssh_project_id\n    autoload: true\n  - name: master\n    expire: 1d\n    path: ~/Work/Keys/master_ssh_key\n```\n\n- `autoload` defaults to False in configuration if not specified.\n- `expore` defines a valid value for key expiration in SSH agent, for example `8h` or `5d`\n\n## Example python code\n\nWith such configuration file, you can load the keys marked as `autoload` to the SSH\nagent with following example code. Calling the load method again does not try loading\nthe keys again (key is detected in agent loaded keys by hash).\n\n```python\nfrom ssh_assets.session import SshAssetSession\nSshAssetSession().load_pending_keys()\n```\n\n## History\n\nThis module replaces previous module `systematic-ssh-config` when ready.\n',
    'author': 'Ilkka Tuohela',
    'author_email': 'hile@iki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hile/ssh-assets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
