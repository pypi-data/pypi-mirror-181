# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['selva',
 'selva._utils',
 'selva.configuration',
 'selva.di',
 'selva.di.service',
 'selva.web',
 'selva.web.converter',
 'selva.web.routing']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['coverage>=6.5.0,<7.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest>=7.2.0,<8.0.0',
 'starlette>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'selva',
    'version': '0.6.0',
    'description': 'ASGI Web Framework with Dependency Injection',
    'long_description': '# Project Selva\n\nDocumentation: https://livioribeiro.github.io/selva/\n\nSelva is a Python ASGI web framework built on top of [asgikit](https://github.com/livioribeiro/asgikit)\nand inspired by Spring Boot, AspNet Core and FastAPI.\n\nIt features a Dependency Inversion system to help build robust and reliable applications.\n\n## Quick start\n\nInstall `selva` and `uvicorn` to run application:\n\n```shell\npip install selva uvicorn[standard]\n```\n\nCreate a module called `application.py`:\n\n```shell\ntouch application.py\n```\n\nCreate a controller:\n\n```python\nfrom selva.web import controller, get\n\n\n@controller\nclass Controller:\n    @get\n    def hello(self):\n        return "Hello, World!"\n```\n\nRun application with `uvicorn` (Selva will automatically load `application.py`):\n\n```shell\nuvicorn selva.run:app --reload\n```\n',
    'author': 'Livio Ribeiro',
    'author_email': 'livioribeiro@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/livioribeiro/selva',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
