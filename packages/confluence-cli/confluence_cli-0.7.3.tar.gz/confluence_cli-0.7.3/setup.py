# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'aiologger>=0.7.0,<0.8.0',
 'atlassian-python-api==3.23.0',
 'click-completion>=0.5.2,<0.6.0',
 'click>=8.1.3,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'python-box>=6.1.0,<7.0.0',
 'python-decouple>=3.6,<4.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'urllib3>=1.26.13,<2.0.0']

setup_kwargs = {
    'name': 'confluence-cli',
    'version': '0.7.3',
    'description': 'Just another Atlassian Confluence API cli extension',
    'long_description': '# confluence-cli\n\nconfluence-cli is a convenient wrapper module for python atlassian confluence original package.\n\n## confluence-cli installation\n\n```shell\n# Desde la raiz del repositorio\npython3 -m pip install  confluence-cli\n```\n\n## Examples\n\n```python\n\nparams = {\n        "baseURL": "http://confluence:8090",\n        "user": "myuser",\n        "password": "mypass",\n        "proxies": {\n            "http": "",\n            "https": ""\n        },\n        "verify_ssl": False\n    }\n\nconfluence_api = ConfluenceWrapper(params)\n# This class method, for example, is not available in original atlassian confluence module.\nconfluence_api.add_content_restrictions("3407893",["read","update"],group_name, "group")\n# This class method, for example, is not available in original atlassian confluence module.\nconfluence_api.add_space_permissions_rpc(space_key="ds",permissions=["SETSPACEPERMISSIONS","EXPORTSPACE"],entity_name=group_name)\n    \n\n```\n',
    'author': 'J. Andres Guerrero',
    'author_email': 'juguerre@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9',
}


setup(**setup_kwargs)
