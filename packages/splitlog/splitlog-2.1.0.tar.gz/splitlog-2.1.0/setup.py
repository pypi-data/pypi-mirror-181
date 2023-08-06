# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitlog']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=5.1.0,<6.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.1']

entry_points = \
{'console_scripts': ['splitlog = splitlog.__main__:main']}

setup_kwargs = {
    'name': 'splitlog',
    'version': '2.1.0',
    'description': 'Utility to split aggregated logs from Apache Hadoop Yarn applications into a folder hierarchy',
    'long_description': 'splitlog\n========\n \nHadoop Yarn application logs aggregate all container logs of a Yarn application into a single file. This makes it very\ndifficult to use Unix command line tools to analyze these logs: Grep will search over all containers and context\nprovided for hits often does not include Yarn container name or host name. `splitlog` splits a combined logfile for all\ncontainers of an application into a file system hierarchy suitable for further analysis:\n\n```\nout\n└── hadoopnode\n    ├── container_1671326373437_0001_01_000001\n    │   ├── directory.info\n    │   ├── launch_container.sh\n    │   ├── prelaunch.err\n    │   ├── prelaunch.out\n    │   ├── stderr\n    │   ├── stdout\n    │   └── syslog\n    ├── container_1671326373437_0001_01_000002\n    │   ├── directory.info\n    │   ├── launch_container.sh\n    │   ├── prelaunch.err\n    │   ├── prelaunch.out\n    │   ├── stderr\n    │   ├── stdout\n    │   └── syslog\n    └── container_1671326373437_0001_01_000003\n        ├── directory.info\n        ├── launch_container.sh\n        ├── prelaunch.err\n        ├── prelaunch.out\n        ├── stderr\n        ├── stdout\n        └── syslog\n\n4 directories, 21 files\n```\n \nInstallation\n------------\nPython 3.7+ must be available. Installation via [pipx](https://pypi.org/project/pipx/):\n\n```shell script\npipx install splitlog\n```\n \nHow to use\n----------\n\nRead logs from standard input:\n```shell script\nyarn logs -applicationId application_1582815261257_232080 | splitlog\n```\n\nRead logs from file `application_1582815261257_232080.log`:\n```shell script\nsplitlog -i application_1582815261257_232080.log\n```\n',
    'author': 'Sebastian Klemke',
    'author_email': 'pypi@nerdheim.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/splitlog/splitlog.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
