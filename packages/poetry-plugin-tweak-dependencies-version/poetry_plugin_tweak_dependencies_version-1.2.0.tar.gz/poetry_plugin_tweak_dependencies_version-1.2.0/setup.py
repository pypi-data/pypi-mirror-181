# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_plugin_tweak_dependencies_version']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.3.0,<1.4.0']

entry_points = \
{'poetry.application.plugin': ['tweak_dependencies_version = '
                               'poetry_plugin_tweak_dependencies_version:Plugin']}

setup_kwargs = {
    'name': 'poetry-plugin-tweak-dependencies-version',
    'version': '1.2.0',
    'description': 'Poetry plugin used to tweak dependency versions',
    'long_description': '# Poetry plugin tweak dependencies version\n\nPlugin use to tweak the dependencies of the project.\n\nWill be used when we have different constraints for the dependencies, like publish and dependency upgrader like Renovate.\n\nThis plugin will let us tweak the dependencies of the published packages.\n\nConfig:\n\n```toml\n[build-system]\nrequires = ["poetry-core>=1.0.0", "poetry-plugin-tweak-dependencies-version"]\nbuild-backend = "poetry.core.masonry.api"\n\n[tool.poetry-plugin-tweak-dependencies-version]\ndefault = "(present|major|minor|patch|full)" # Default to `full`\n"<package>" = "(present|major|minor|patch|full|<alternate>)"\n\n```\n\n`present` => `*`, `major` => `x.*`, `minor` => `x.y.*`, `patch` => `x.y.z`, `full` => keep the original version.\nOr just specify an alternate version constraint.\n',
    'author': 'Stéphane Brunner',
    'author_email': 'stephane.brunner@camptocamp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sbrunner/poetry-plugin-tweak-dependencies-version',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
