# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mistelaflask',
 'mistelaflask.views',
 'mistelaflask.views.admin_views',
 'mistelaflask.views.guest_views']

package_data = \
{'': ['*'],
 'mistelaflask': ['templates/*',
                  'templates/admin/*',
                  'templates/admin/events/*',
                  'templates/admin/guests/*',
                  'templates/admin/invitations/*',
                  'templates/admin/locations/*',
                  'templates/admin/main_events/*',
                  'templates/auth/*',
                  'templates/guest/*',
                  'templates/guest/events/*']}

install_requires = \
['Flask-Login>=0.6.2,<0.7.0',
 'Flask-Mail>=0.9.1,<0.10.0',
 'Flask>=2.2.2,<3.0.0',
 'commitizen>=2.35.0,<3.0.0',
 'flask-sqlalchemy>=3.0.2,<4.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pyOpenSSL>=22.1.0,<23.0.0']

entry_points = \
{'console_scripts': ['add_test_users = '
                     'scripts.generate_initial_db:generate_test_data',
                     'init_mistelaflask = '
                     'scripts.generate_initial_db:init_mistelaflask',
                     'wsgi = wsgi:init_mistelaflask']}

setup_kwargs = {
    'name': 'mistela-flask',
    'version': '0.16.1',
    'description': 'A multi-event planner flask application. It allows for RSVP options, authentication, and guest management',
    'long_description': '![GitHub release (latest by date)](https://img.shields.io/github/v/release/carsopre/mistela-flask)\n![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/carsopre/mistela-flask)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# mistela-flask\nA multi-event planner elaborated with Flask.\n\nInitial steps done following this [Digital Ocean guide](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-7-setting-up-the-authorization-function)\n\nThis version of `Flask` aims to provide a simpile solution to manage an event such as a wedding with different \'sub-events\'. The tool also provides a custom-defined admin page as `Flask` does not really provide one itself (and I did not like `Flask-admin` as all users seemed to have admin rights).\n\nEither way, this was a nice user-case for me to get hands-on with Flask.\n\n## Why the name Mistela?\nMistela is \'sort of a wine\' quite common in my region (València, Spain) for celebrations or simply after a family dinner. It made sense that if this flask \'flavour\' is about events (celebrations) management, it should have an appropiate name, therefore, mistela-flask :).\n\n## Downloading the package.\n* Directly from the source:\n```cli\npip install git+https://github.com/Carsopre/mistela-flask.git\n```\n* Or from pypi:\n```cli\npip install mistela-flask\n```\n\n## Installing the repository.\nTo develop on the repository you should be using `Poetry`. Once installed, simply run the install command`poetry install` and all development and production dependencies will be added to your virtual environment.\n\n## Usage\nMistela-flask can be used as a package and easily deployed as any regular flask app.\n```python\nfrom mistelaflask import create_app\nimport secrets\nimport os\nos.environ["SECRET_KEY"] = secrets.token_hex(16) # Required environment variable.\nos.environ["DATABASE_URI"] = "sqlite:///db.sqlite"\nos.environ["MISTELA_TITLE"] = "My big event"\nos.environ["STATIC_FOLDER"] = "path//to//my//static//folder"\nos.environ["MAIL_USERNAME"] = "joe.doe@email.com"\nos.environ["MAIL_PASSWORD"] = "1234"\n\napp = create_app() \napp.run()\n```\n> By default, mistelaflask will run on a `SQLite` database.\n\nA more \'real\' example can be found in the root of the repository as `wsgi.py`.\n\n\n',
    'author': 'Carles S. Soriano Perez',
    'author_email': 'sorianoperez.carles@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/carsopre/mistela-flask',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
