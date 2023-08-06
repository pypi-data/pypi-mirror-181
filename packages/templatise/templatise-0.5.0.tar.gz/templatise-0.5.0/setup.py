# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['templatise']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'click-log>=0.4.0,<0.5.0',
 'click>=8.1.3,<9.0.0',
 'requests>=2.28.1,<3.0.0',
 'retry>=0.9.2,<0.10.0',
 'toml-sort>=0.20.1,<0.21.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['initialise = templatise.initialise:main']}

setup_kwargs = {
    'name': 'templatise',
    'version': '0.5.0',
    'description': 'You can use template.py to create a new GitHub repository.',
    'long_description': '# template.py\n\n[Homepage][repository]\n\nBy Alex Brandt <alunduil@gmail.com>\n\n## Description\n\nYou can use template.py to create a new GitHub repository.  The repository will\nhave poetry, VS Code devcontainers, and various GitHub actions ready to use.\n\ntemplate.py is related to [Cookiecutter] because both are templates for\nbootstrapping projects.  template.py allows you to have a full development\nenvironment with only VS Code and it\'s "Remote Development" plugin.\n[Cookiecutter] expects you to re-use your development environment for multiple\nprojects.\n## Terms of use\n\nYou are free to use template.py as a basis for your own projects without any\nconditions.  See the [LICENSE] file for details.\n\n## Prerequisites\n\n1. VS Code with "Remote Development" installed\n\n## How to use this template\n\n1. Visit [the repository][repository]\n1. Click "Use this template"\n1. Follow the GitHub Docs to [Create a repo][create a repo]\n1. Open VS Code\n1. Open the command prompt (ctrl+shift+p)\n1. Type "clone repository in container" and hit return\n1. Input the GitHub URL of your new repository\n1. In the resulting terminal (ctrl+\\`), run: `poetry run initialise`\n1. Resolve the README update issue that is generated\n1. Continue working on your awesome project\n\n## Documentation\n\n* [LICENSE]: The license governing use of template.py\n\n## Getting Help\n\n* [GitHub Issues][issues]: Support requests, bug reports, and feature requests\n\n## How to Help\n\n* Submit [issues] for problems or questions\n* Submit [pull requests] for proposed changes\n\n[create a repo]: https://docs.github.com/en/get-started/quickstart/create-a-repo\n[issues]: https://github.com/alunduil/template.py/issues\n[LICENSE]: ./LICENSE\n[pull requests]: https://github.com/alunduil/template.py/pulls\n[repository]: https://github.com/alunduil/template.py\n[Cookiecutter]: https://github.com/cookiecutter/cookiecutter\n',
    'author': 'Alex Brandt',
    'author_email': 'alunduil@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alunduil/template.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
