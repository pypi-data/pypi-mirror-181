# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pg4n', 'pg4n.test']

package_data = \
{'': ['*']}

install_requires = \
['myst-parser>=0.18.1,<0.19.0',
 'pexpect>=4.8.0,<5.0.0',
 'psycopg[binary]>=3.1.3,<4.0.0',
 'pyparsing>=3.0.9,<4.0.0',
 'pyte>=0.8.1,<0.9.0',
 'pytest-postgresql>=4.1.1,<5.0.0',
 'pytest>=7.1.3,<8.0.0',
 'sphinx-autodoc-typehints>=1.19.4,<2.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0',
 'sphinx>=5.2.3,<6.0.0',
 'sqlglot>=6.3.2,<7.0.0']

entry_points = \
{'console_scripts': ['pg4n = pg4n:main.main']}

setup_kwargs = {
    'name': 'pg4n',
    'version': '0.1.2.dev37',
    'description': 'PostgreSQL for novices - helps debug PostgreSQL queries',
    'long_description': "# PostgreSQL for novices\n\n[📄 Documentation](https://project-c-sql.github.io/)\n\nThis README is meant for developers of the project, and not for end users. For end users, please see the documentation linked above.\n\n- [PostgreSQL for novices](#postgresql-for-novices)\n  - [Notes for developers](#notes-for-developers)\n    - [Poetry](#poetry)\n      - [Versioning](#versioning)\n    - [Imports](#imports)\n    - [Running tests](#running-tests)\n      - [Using docker](#using-docker)\n    - [Building documents](#building-documents)\n    - [Linting](#linting)\n\n## Notes for developers\n\n### Poetry\n\nThis project uses [Poetry](https://python-poetry.org/) for packaging. Although one should refer to [Poetry docs](https://python-poetry.org/docs/) for a thorough introduction, here's a short summary of the intended workflow with Poetry:\n\n- To install all dependencies and the application, type `poetry install`. After installation, if the Python scripts folder is in your PATH, you should be able to invoke `main.main()` with `pg4n`.\n- To make VS Code use Poetry's virtual environment, type `poetry env info`, copy virtual environment executable path, press F1 and type `Python: Select Interpreter` > `Enter interpreter path...` > paste path and press `<ENTER>`.\n- To add/remove a dependency, type `poetry add <dep>`/`poetry remove <dep>`.\n- To execute a command from within virtual environment shell, type `poetry run <cmd>`.\n- To enter a shell session within the Poetry virtual environment, type `poetry shell`.\n\n#### Versioning\n\nYou can bump the version number automatically with `poetry version patch`, `poetry version minor`, etc. See `poetry version -h`.\n\nSee version history [here](https://pypi.org/project/pg4n/#history).\n\n### Imports\n\nDuring development, you must run the program as a module, e.g., `poetry run python -m src.pg4n.main`, so that the imports work.\n\n### Running tests\n\nHaving PostgreSQL running on port 5432, do `poetry run pytest`.\n\nYou may need to provide environment variables that match your config:\n\n| Variable     | Default value   | Description                                             |\n| ------------ | --------------- | ------------------------------------------------------- |\n| `PGHOST`     | `127.0.0.1`     | Hostname of the PostgreSQL server.                      |\n| `PGPORT`     | `5432`          | Port to an active PostgreSQL instance.                  |\n| `PGUSER`     | `postgres`      | The user that will be used to manage the test database. |\n| `PGPASSWORD` |                 | Password, in case password authentication is used.      |\n| `PGDBNAME`   | `test_database` | Database name.                                          |\n \nFor example, if PostgreSQL is on port 5433, just do `PGPORT=5433 poetry run pytest` (Bash syntax).\n\n#### Using docker\n\nTo get a similar PostgreSQL instance as with GitHub Actions workflow:<br>\n`docker run --rm -P -p 127.0.0.1:5432:5432 --name pg -e POSTGRES_PASSWORD=postgres -d postgres:14.5-alpine`\n\nYou'll need to tell pytest the password: `PGPASSWORD=postgres poetry run pytest`.\n\n### Building documents\n\n1. If `docs/api` is not up-to-date or doesn't exist, run:<br>`poetry run sphinx-apidoc -f -o docs/api src/pg4n '*/test*'`\n2. To generate the documentation:<br>`poetry run sphinx-build -b html docs docs/build`\n\nNote that the GitHub Pages site is only updated on pushes to `main` branch.\n\n### Linting\n\nFor linting, you need the CI tools: `poetry install --with=ci`. The tools used are:\n- `black` for formatting\n- `pylint` for linting\n- `mypy` for static type checking\n- `isort` for sorting imports\n\nTo get a grade that the CI/CD pipeline would give you, you can do `poetry run scripts/ci-grade.sh` to run all the checks. The output is possibly long, so pipe it to a file perusal filter such as `less` to scroll through it and search for things of concern, e.g., `summary` to see scores.\n",
    'author': 'Jesper Niemelä',
    'author_email': 'jesper.niemela@tuni.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
