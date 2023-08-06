# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helper_auth']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2,<3']

setup_kwargs = {
    'name': 'helper-auth',
    'version': '0.2.0',
    'description': 'Requests authentication using existing helpers',
    'long_description': "[![helper-auth on PyPI](https://img.shields.io/pypi/v/helper-auth)][PyPI]\n\n# Installation\n\n```\npip install helper-auth\n```\n\n# Usage\n\nObjects of the `HelperAuth` class are intended to be used as custom\nauthentication handlers as per the\n[Requests documentation](https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication).\n\n\n## Default scenario\n\nSuppose you have an existing GitHub personal access token, and a\n[Git credential helper](https://git-scm.com/docs/gitcredentials#_custom_helpers)\nalready set up for Git to authenticate to GitHub using this token as\nthe password. This helper is named `git-credential-github` and prints\nthe following to standard output:\n\n```\nusername=your_github_username\npassword=your_github_token\n```\n\nYou want to use the same token to make GitHub API calls in Python with\nthe help of the Requests library. The API expects a\n`token your_github_token` string as the value of\nyour request's `Authorization` header.\n\nYou can use `HelperAuth` with its default settings:\n\n```python\nimport requests\nfrom helper_auth import HelperAuth\n\nheaders = {'Accept': 'application/vnd.github+json'}\nauth = HelperAuth('git-credential-github')\n\nresponse = requests.get(\n    'https://api.github.com/user/repos',\n    headers=headers,\n    auth=auth,\n)\n```\n\n[PyPI]: https://pypi.org/project/helper-auth\n",
    'author': 'Michal Porteš',
    'author_email': 'michalportes1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mportesdev/helper-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
