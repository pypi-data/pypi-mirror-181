# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fractal_server',
 'fractal_server.app',
 'fractal_server.app.api',
 'fractal_server.app.api.v1',
 'fractal_server.app.db',
 'fractal_server.app.models',
 'fractal_server.app.runner',
 'fractal_server.app.runner._parsl',
 'fractal_server.app.runner._process',
 'fractal_server.app.runner._slurm',
 'fractal_server.app.security',
 'fractal_server.common',
 'fractal_server.common.schemas',
 'fractal_server.migrations',
 'fractal_server.migrations.versions',
 'fractal_server.tasks']

package_data = \
{'': ['*'], 'fractal_server': ['misc/*']}

install_requires = \
['SQLAlchemy-Utils>=0.38.3,<0.39.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'alembic>=1.8.0,<2.0.0',
 'fastapi-users-db-sqlmodel>=0.2.0,<0.3.0',
 'fastapi-users[oauth]>=10.1.1,<11.0.0',
 'fastapi>=0.78.0,<0.79.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'sqlmodel>=0.0.8,<0.0.9',
 'uvicorn>=0.18.2,<0.19.0']

extras_require = \
{'gunicorn': ['gunicorn>=20.1.0,<21.0.0'],
 'postgres': ['asyncpg>=0.27.0,<0.28.0', 'psycopg2>=2.9.5,<3.0.0'],
 'slurm': ['clusterfutures>=0.4,<0.5']}

entry_points = \
{'console_scripts': ['fractal-server = fractal_server.__main__:run',
                     'openapi = fractal_server.__main__:save_openapi']}

setup_kwargs = {
    'name': 'fractal-server',
    'version': '1.0.0b5',
    'description': 'Server component of the Fractal analytics platform',
    'long_description': '# Fractal Server\n\n[![PyPI version](https://img.shields.io/pypi/v/fractal-server?color=gree)](https://pypi.org/project/fractal-server/)\n[![CI Status](https://github.com/fractal-analytics-platform/fractal-server/actions/workflows/ci.yml/badge.svg)](https://github.com/fractal-analytics-platform/fractal-server/actions/workflows/ci.yml)\n[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\nFractal is a framework to process high content imaging data at scale and prepare it for interactive visualization.\n\n![Fractal_Overview](https://fractal-analytics-platform.github.io/assets/fractal_overview.jpg)\n\nThis is the server component of the fractal analytics platform. If you are interested in the client component, please refer to the [main\nrepository](https://github.com/fractal-analytics-platform/fractal). If you are interested in the fractal tasks, please refer to [the tasks repository](https://github.com/fractal-analytics-platform/fractal-tasks-core).\n\n## Documentation\n\nSee https://fractal-analytics-platform.github.io/fractal-server.\n\n## Development\n\n### Setting up environment\n\nWe use [poetry](https://python-poetry.org/docs/) (v1.2) to manage the development environment and the dependencies. Running\n```\npoetry install [--with dev] [-E slurm]\n```\nwill take care of installing all the dependencies in a separate environment,\noptionally installing also the development dependencies.\n\nIt may be useful to use a different interpreter from the one installed in your\nsystem. To this end we recommend using\n[pyenv](https://github.com/pyenv/pyenv). In the project folder, invoking\n```\npyenv local 3.8.13\npoetry env use 3.8\npoetry install\n```\nwill install Fractal in a development environment using `python 3.8.13` instead\nof the system-wide interpreter.\n\n### Testing\n\nWe use [pytest](https://docs.pytest.org/en/7.1.x/) for unit and integration\ntesting of Fractal. If you installed the development dependencies, you may run\nthe test suite by invoking\n```\npoetry run pytest\n```\n\n# Contributors and license\n\nUnless otherwise stated in each individual module, all Fractal components are released according to a BSD 3-Clause License, and Copyright is with Friedrich Miescher Institute for Biomedical Research and University of Zurich.\n\nThe SLURM compatibility layer is based on [`clusterfutures`](https://github.com/sampsyo/clusterfutures), by [@sampsyo](https://github.com/sampsyo) and collaborators, and it is released under the terms of the MIT license.\n\nFractal was conceived in the Liberali Lab at the Friedrich Miescher Institute for Biomedical Research and in the Pelkmans Lab at the University of Zurich (both in Switzerland). The project lead is with [@gusqgm](https://github.com/gusqgm) & [@jluethi](https://github.com/jluethi). The core development is done under contract by [@mfranzon](https://github.com/mfranzon), [@tcompa](https://github.com/tcompa) & [@jacopo-exact](https://github.com/jacopo-exact) from [eXact lab S.r.l.](exact-lab.it).\n',
    'author': 'Jacopo Nespolo',
    'author_email': 'jacopo.nespolo@exact-lab.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fractal-analytics-platform/fractal-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
