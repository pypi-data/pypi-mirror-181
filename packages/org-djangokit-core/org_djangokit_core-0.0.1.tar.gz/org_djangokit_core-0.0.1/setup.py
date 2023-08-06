# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djangokit',
 'djangokit.core',
 'djangokit.core.test',
 'djangokit.core.test.routes',
 'djangokit.core.test.routes._slug',
 'djangokit.core.test.routes.catchall',
 'djangokit.core.views']

package_data = \
{'': ['*'],
 'djangokit.core': ['static/*',
                    'static/build/*',
                    'templates/djangokit/*',
                    'templates/djangokit/base/*'],
 'djangokit.core.test.routes': ['docs/*', 'docs/_slug/*']}

install_requires = \
['Django>=3.0', 'python-dotenv>=0.21.0']

setup_kwargs = {
    'name': 'org-djangokit-core',
    'version': '0.0.1',
    'description': 'DjangoKit core',
    'long_description': '# DjangoKit Core\n\nThis package implements the core functionality of DjangoKit.\n\nTODO:\n\nFor more information...\n',
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
