# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypothesis_requests', 'hypothesis_requests.strategies']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis>=6.61.0,<7.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'hypothesis-requests',
    'version': '0.1.0',
    'description': 'You can use hypothesis-requests to create a new GitHub repository.',
    'long_description': '# hypothesis-requests\n\n[Homepage][repository]\n\nBy Alex Brandt <alunduil@gmail.com>\n\n## Description\n\nYou can use hypothesis-requests to generate [request] objects for hypothesis\nbased tests.\n\n## Terms of use\n\nSee the [LICENCE] file for details.\n\n## Prerequisites\n\n1. Hypothesis property based tests\n\n## How to use this template\n\n1. Add hypothesis-requests to your project dependencies.\n1. Utilise hypothesis_requests.strategies to generate Requests, Responses, etc.\n\n## Documentation\n\n* [LICENSE]: The license governing use of template.py\n\n## Getting Help\n\n* [GitHub Issues][issues]: Support requests, bug reports, and feature requests\n\n## How to Help\n\n* Submit [issues] for problems or questions\n* Submit [pull requests] for proposed changes\n\n[create a repo]: https://docs.github.com/en/get-started/quickstart/create-a-repo\n[issues]: https://github.com/alunduil/hypothesis-requests/issues\n[LICENSE]: ./LICENSE\n[pull requests]: https://github.com/alunduil/hypothesis-requests/pulls\n[repository]: https://github.com/alunduil/hypothesis-requests\n[Cookiecutter]: https://github.com/cookiecutter/cookiecutter\n',
    'author': 'alunduil',
    'author_email': 'alunduil@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alunduil/hypothesis-requests',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
