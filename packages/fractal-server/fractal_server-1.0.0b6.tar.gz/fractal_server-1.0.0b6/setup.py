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
    'version': '1.0.0b6',
    'description': 'Server component of the Fractal analytics platform',
    'long_description': '# Fractal Server\n\n[![PyPI version](https://img.shields.io/pypi/v/fractal-server?color=gree)](https://pypi.org/project/fractal-server/)\n[![CI Status](https://github.com/fractal-analytics-platform/fractal-server/actions/workflows/ci.yml/badge.svg)](https://github.com/fractal-analytics-platform/fractal-server/actions/workflows/ci.yml)\n[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\nFractal is a framework to process high content imaging data at scale and\nprepare it for interactive visualization.\n\n![Fractal_Overview](https://fractal-analytics-platform.github.io/assets/fractal_overview.jpg)\n\nThis is the server component of the fractal analytics platform. If you are\ninterested in the client component, please refer to the\n[main repository](https://github.com/fractal-analytics-platform/fractal). If\nyou are interested in the fractal tasks, please refer to\n[the tasks repository](https://github.com/fractal-analytics-platform/fractal-tasks-core).\n\n## Documentation\n\nSee https://fractal-analytics-platform.github.io/fractal-server.\n\n# Contributors and license\n\nUnless otherwise stated in each individual module, all Fractal components are\nreleased according to a BSD 3-Clause License, and Copyright is with Friedrich\nMiescher Institute for Biomedical Research and University of Zurich.\n\nThe SLURM compatibility layer is based on\n[`clusterfutures`](https://github.com/sampsyo/clusterfutures), by\n[@sampsyo](https://github.com/sampsyo) and collaborators, and it is released\nunder the terms of the MIT license.\n\nFractal was conceived in the Liberali Lab at the Friedrich Miescher Institute\nfor Biomedical Research and in the Pelkmans Lab at the University of Zurich\n(both in Switzerland). The project lead is with\n[@gusqgm](https://github.com/gusqgm) & [@jluethi](https://github.com/jluethi).\nThe core development is done under contract by\n[@mfranzon](https://github.com/mfranzon), [@tcompa](https://github.com/tcompa)\n& [@japs](https://github.com/japs) of [eXact lab S.r.l.](exact-lab.it).\n',
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
