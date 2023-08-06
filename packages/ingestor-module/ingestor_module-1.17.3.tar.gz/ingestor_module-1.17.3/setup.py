# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ingestor',
 'ingestor.common',
 'ingestor.content_profile',
 'ingestor.content_profile.network',
 'ingestor.merge_df',
 'ingestor.rce_user_cluster',
 'ingestor.repository',
 'ingestor.sample',
 'ingestor.user_content_network',
 'ingestor.user_profile',
 'ingestor.user_profile.main',
 'ingestor.user_profile.network',
 'ingestor.user_profile.preferences',
 'ingestor.user_profile.preprocessing',
 'ingestor.user_profile.streaming_clustering',
 'ingestor.user_rating',
 'ingestor.utils']

package_data = \
{'': ['*']}

install_requires = \
['Sastrawi>=1.0.1,<2.0.0',
 'boto3>=1.20.50,<2.0.0',
 'graphdb-module>=0.12.14,<0.13.0',
 'networkx>=2.8.5,<3.0.0',
 'nltk>=3.7,<4.0',
 'numpy>=1.22.1,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'setuptools>=59.1.1,<60.0.0']

setup_kwargs = {
    'name': 'ingestor-module',
    'version': '1.17.3',
    'description': '',
    'long_description': '# rce_ingestor_module\n\n',
    'author': 'AIML Team',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
