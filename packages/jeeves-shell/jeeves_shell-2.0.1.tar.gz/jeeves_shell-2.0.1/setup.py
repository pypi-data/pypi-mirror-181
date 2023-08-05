# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jeeves_shell']

package_data = \
{'': ['*']}

install_requires = \
['documented>=0.1.1,<0.2.0',
 'more-itertools>=9.0.0,<10.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['j = jeeves_shell.cli:app']}

setup_kwargs = {
    'name': 'jeeves-shell',
    'version': '2.0.1',
    'description': 'Pythonic replacement for GNU Make',
    'long_description': '# Jeeves Shell\n\n[![Build Status](https://github.com/jeeves-sh/jeeves-shell/workflows/test/badge.svg?branch=master&event=push)](https://github.com/jeeves-sh/jeeves-shell/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/jeeves-sh/jeeves-shell/branch/master/graph/badge.svg)](https://codecov.io/gh/jeeves-sh/jeeves-shell)\n[![Python Version](https://img.shields.io/pypi/pyversions/jeeves-shell.svg)](https://pypi.org/project/jeeves-shell/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nA Pythonic replacement for GNU Make, with re-usability and modularity added as a bonus.\n\n\n## Installation\n\n```bash\npip install jeeves-shell\n```\n\n## License\n\n[MIT](https://github.com/jeeves-sh/jeeves-shell/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package).\n\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jeeves-sh/jeeves-shell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
