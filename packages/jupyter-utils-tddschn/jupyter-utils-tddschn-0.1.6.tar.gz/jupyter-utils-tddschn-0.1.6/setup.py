# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyter_utils_tddschn']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.11.2,<3.0.0',
 'ipykernel>=6.13.0,<7.0.0',
 'ipython>=8.2.0,<9.0.0',
 'nbformat>=5.3.0,<6.0.0']

setup_kwargs = {
    'name': 'jupyter-utils-tddschn',
    'version': '0.1.6',
    'description': '',
    'long_description': "# jupyter-utils-tddschn\n\nMost code were copied from https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html\n\n## How do I ... ?\n\n### Import a `.ipynb` file?\n\n```python\nfrom jupyter_utils_tddschn import notebook_importer\n\n# then just import a .ipynb file like a .py file\n# to import test.ipynb:\nimport test\n```\n\n### Show the content of a notebook, syntax highlighted?\n\n```python\nfrom jupyter_utils_tddschn.notebook_shower import show_notebook\n\nshow_notebook('notebooks/test.ipynb')\n\n```",
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/jupyter-utils-tddschn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
