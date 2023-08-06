# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osin',
 'osin.apis',
 'osin.controllers',
 'osin.formats',
 'osin.integrations',
 'osin.models',
 'osin.models.migration',
 'osin.models.report',
 'osin.types']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'gena>=1.6.4,<2.0.0',
 'h5py>=3.7.0,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'orjson>=3.8.2,<4.0.0',
 'peewee>=3.15.2,<4.0.0',
 'psutil>=5.9.2,<6.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'ream2>=1.5.4,<2.0.0',
 't2-yada>=1.0.4,<2.0.0',
 'tornado>=6.2,<7.0']

setup_kwargs = {
    'name': 'osin',
    'version': '1.9.1',
    'description': 'Research and Experiments',
    'long_description': "# osin &middot; [![PyPI](https://img.shields.io/pypi/v/osin)](https://pypi.org/project/osin)\n\nThere are existing systems (e.g., neptune.ai, sacred) helping you organize, log data of your experiments. However, typically, the tasks of running the experiments are your responsible to bear. If you update your code and need to re-run your experiments, you may want to delete previous runs, which would be painful to have to do manually many times.\n\nWe rethink the experimenting process. Why don't we start with specifying the designed report (e.g., charts) and how to run/query to get the numbers to fill the report? This would free ones from manually starting/running the experiments and managing the experiment data. `osin` is a tool that helps you to achieve that goal.\n\nNote: this tool is expected to use locally or inside VPN network as it doesn't provide any protection against attackers.\n\n## Quick start\n\nStart the application:\n\n```bash\nDBFILE=%PATH_TO_DBFILE% python -m osin.main\n```\n\nOr start the services manually:\n\n```bash\nexport DBFILE=%PATH_TO_DBFILE%\npython -m osin.worker # start worker to run jobs\npython -m osin.server # start the server so clients can send job result\nstreamlit run osin/ui/dashboard.py # start a dashboard to view/create reports\n```\n\nYou will start by designing the output that your experiments will produce. For example:\n\n```yaml\n\n```\n",
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
