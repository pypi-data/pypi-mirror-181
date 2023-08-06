# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_forms_plus']

package_data = \
{'': ['*'], 'django_forms_plus': ['static/django_forms_plus/*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'django-forms-plus',
    'version': '0.1.1',
    'description': 'React-powered forms for Django',
    'long_description': "# Django-Forms-Plus (dfplus)\n\nThe extendable ReactJS powered frontend for Django Forms \ncontroled by forms.BaseForm native declarations with some additions.\n\nDefine your forms in python code as usually you do and get React powered forms UI\nalmost for free ;)\n\n## Features\n- how to define a form? like a regular `forms.BaseForm` with some additions\n- how are forms submitted? via AJAX\n- validation & errors \n- fieldsets (layouts)\n- customization\n  - Python: use regular Django's idiomatic patterns/approaches around `django.forms` with some additions\n  - JS: React code was build with extensibility in mind\n  - CSS: use regular CSS classes, add your own. No CSS-in-JS (it's a by design decision)\n",
    'author': 'Vladimir Sklyar',
    'author_email': 'versus.post@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/versusbassz/django_forms_plus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
