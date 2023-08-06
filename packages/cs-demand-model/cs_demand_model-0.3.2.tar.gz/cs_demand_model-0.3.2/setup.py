# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cs_demand_model',
 'cs_demand_model.config',
 'cs_demand_model.data',
 'cs_demand_model.data.ssda903',
 'cs_demand_model.datastore',
 'cs_demand_model.fixtures',
 'cs_demand_model.fixtures.config',
 'cs_demand_model.rpc',
 'cs_demand_model.rpc.figs',
 'cs_demand_model.rpc.forms',
 'cs_demand_model.rpc.views',
 'cs_demand_model_samples']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'fs>=2.4.16,<3.0.0',
 'numpy==1.22.4',
 'pandas==1.4.2',
 'python-dateutil>=2.8.2,<3.0.0',
 'rpc-wrap[cli]>=0.3.0,<0.4.0']

extras_require = \
{'cli': ['matplotlib>=3.5.2,<4.0.0',
         'tqdm>=4.64.1,<5.0.0',
         'openpyxl>=3.0.10,<4.0.0'],
 'jupyter': ['matplotlib>=3.5.2,<4.0.0',
             'tqdm>=4.64.1,<5.0.0',
             'jupyterlab>=3.4.8,<4.0.0',
             'openpyxl>=3.0.10,<4.0.0',
             'plotly>=5.11.0,<6.0.0'],
 'pyodide': ['openpyxl>=3.0.10,<4.0.0', 'plotly>=5.11.0,<6.0.0'],
 'web': ['Flask>=2.1.2,<3.0.0', 'Flask-Cors>=3.0.10,<4.0.0']}

setup_kwargs = {
    'name': 'cs-demand-model',
    'version': '0.3.2',
    'description': "Python port of Social Finance's children's social care demand model",
    'long_description': 'None',
    'author': 'dezog',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
