# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlh_utils']

package_data = \
{'': ['*']}

install_requires = \
['graphframes-wrapper>=0.6,<0.7',
 'graphframes>=0.6,<0.7',
 'importlib_metadata>=4.8.3,<5.0.0',
 'jellyfish>=0.9,<0.10',
 'pandas>=0.20.1,<0.21.0']

setup_kwargs = {
    'name': 'dlh-utils',
    'version': '0.2.4',
    'description': 'A PySpark package used to expedite and standardise the data linkage process',
    'long_description': "# DLH_utils\n\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)\n[![PyPI version](https://badge.fury.io/py/dlh_utils.svg)](https://badge.fury.io/py/dlh_utils)\n[![PyPi Python Versions](https://img.shields.io/pypi/pyversions/dlh-utils.svg)](https://pypi.python.org/pypi/dlh-utils/)\n\nA Python package produced by the Linkage Development team from the Data Linkage Hub at Office for National Statistics (ONS) containing a set of functions used to expedite and streamline the data linkage process.\n\nIt's key features include:\n* it's scalability to large datasets, using `spark` as a big-data backend\n* profiling and flagging functions used to describe and highlight issues in data\n* standardisation and cleaning functions to make data comparable ahead of linkage\n* linkage functions to derive linkage variables and join data together efficiently\n\nPlease log an issue on the issue board or contact any of the active contributors with any issues or suggestions for improvements you have.\n\n## Installation steps\nDLH_utils supports Python 3.6+. To install the latest version, simply run:\n```sh\npip install dlh_utils\n```\n\n## Using the cluster function\n\nThe cluster function uses Graphframes, which requires an extra JAR file dependency to be submitted to your spark context in order for it to run.\n\nWe have published a graphframes-wrapper package on Pypi that contains this JAR file. This is included in the package requirements\nas a dependency.\n\nIf outside of ONS and this dependency doesn't work, you will need to submit graphframes' JAR file dependency to your spark context. This can be found here:\n\nhttps://repos.spark-packages.org/graphframes/graphframes/0.6.0-spark2.3-s_2.11/graphframes-0.6.0-spark2.3-s_2.11.jar\n\nOnce downloaded, this can be submitted to your spark context by adding this parameter to your SparkSession config: \n\n```sh\nspark.conf.set('spark.jars', path_to_jar_file)\n```\n\n## Thanks\n\nThanks to all those in the Data Linkage Hub, Data Engineering and Methodology at ONS that have contributed towards this repository.\n",
    'author': 'Anthony Edwards',
    'author_email': 'anthonygedwards93@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Data-Linkage/dlh_utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
