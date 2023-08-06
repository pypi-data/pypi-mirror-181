# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['port_forward_manager']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Pygments>=2.13.0,<3.0.0',
 'SQLAlchemy>=1.4.44,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'commonmark>=0.9.1,<0.10.0',
 'pydantic>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'shellingham>=1.5.0,<2.0.0',
 'simplejson>=3.17.6,<4.0.0',
 'sshconf>=0.2.5,<0.3.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pfm = port_forward_manager.cli:run']}

setup_kwargs = {
    'name': 'port-forward-manager',
    'version': '3.0.1',
    'description': 'Port forwarding manager',
    'long_description': '# Port Forward Manager (PFM)\nPFM allows quick and easy management of ports forwarded over SSH (local or remote).\n\n# Installation\n\n```\n# Install tmux\nbrew install tmux\n# Install python poetry https://python-poetry.org/docs/\nbrew install poetry\nor\ncurl -sSL https://install.python-poetry.org | python3 -\n\n# Install PFM\npip install --upgrade port-forward-manager\n\n\n```\n\nSettings file is stored in ~/.ssh/pfm.settings.yaml\n\n## Configure autocomplete\n\nAdd to end of ~/.zshrc\n\n```\nfpath+=~/.zfunc\n\nautoload -Uz compinit\ncompinit\nzstyle \':completion:*\' menu select\n\n```\n\nGenerate autocomplete configuration\n\n```\npfm --install-completion\nsource .zshrc\n```\n# About\n## Settings\nPFM will automatically generate a default configuration file and update new settings to their default values.\n\n\n### show_schema_link\nToggle the ability to show/hide the schema when showing the list of schemas.\n### wait_after_start \nHow long, in seconds, to wait after starting sessions.\n### table_border\nToggle the table border\n### show_pid\nToggle the screen PID\n\nExample settings file:\n```\nschemas:\n    local_proxy:\n      - hostname: some.proxy.host\n        remote_port: 8888\n        type: local\n    remote-server:\n      - hostname: example.host\n        local_port: 1234\n        remote_port: 8080\n        type: local\n      - hostname: example.host\n        local_port: 8888\n        remote_port: 8888\n        type: local\nshow_pid: \'false\'\nshow_schema_link: \'false\'\ntable_border: \'true\'\nwait_after_start: \'0.5\'\nwait_after_stop: 0.5\n```\n\n## Commands\n### config\nShow active sessions\n### forward\nStart a forwarding session\n### schemas\nList configured schemas\n### shutdown\nStop all active sessions\n### start\nStart a schema of forwarding sessions\n### status\nShow active sessions\n### stop\nStop sessions from active schema, host or port\n###version\nShow installed version\n\n# Development\nSetup development environment\n```\ngit clone git@github.com:kxiros/port-forward-manager.git\ncd port-forward-manager\npoetry shell\npoetry install\n```\n\nBuilding python package\n\n```\npython -m build\n```\n\n\nTo Install development version:\n\n```\npip install -e cloned_directory_path\n```\n\nRelease\n```\n#Example to github\ngh release create 1.3 dist/port-forward-manager-1.3.tar.gz -t "Minor fixes" --generate-notes\n\n#Publish on Pypi\n# Configure pypi token\n# poetry config pypi-token.pypi <token>\npoetry publish\n```',
    'author': 'Vladimiro Casinha',
    'author_email': 'vcasinha@kjoo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kxiros/port-forward-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
