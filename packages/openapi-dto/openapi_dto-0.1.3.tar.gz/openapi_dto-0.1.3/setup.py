# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['openapi_dto', 'openapi_dto.engine']

package_data = \
{'': ['*']}

install_requires = \
['camel-converter>=3.0.0,<4.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['openapi_dto = openapi_dto.cli:app']}

setup_kwargs = {
    'name': 'openapi-dto',
    'version': '0.1.3',
    'description': 'A CLI tool for automated DTO generation using OpenAPI schema',
    'long_description': "# openapi-dto\n\nThis small library allows generating Python DTOs from the OpenAPI schema \ndefinition. By default, it uses dataclasses, but it's open for extensions\nand using libraries like pydantic instead.\n\nAfter installation, it might be called in the following way:\n\n```bash\nopenapi_dto \\\n  --naming-convention=camel \\\n  https://foobar.com/api/schema/\n```\n",
    'author': 'Kacper Łukawski',
    'author_email': 'kacper.lukawsk@embassy.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
