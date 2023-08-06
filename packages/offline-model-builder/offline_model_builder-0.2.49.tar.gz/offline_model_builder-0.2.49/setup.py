# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['offline_model_builder',
 'offline_model_builder.common',
 'offline_model_builder.content_profile',
 'offline_model_builder.content_profile.multiclass_image_classification',
 'offline_model_builder.content_profile.multiclass_image_classification.common',
 'offline_model_builder.content_profile.multiclass_image_classification.common.callbacks',
 'offline_model_builder.content_profile.multiclass_image_classification.common.io',
 'offline_model_builder.content_profile.multiclass_image_classification.common.nn',
 'offline_model_builder.content_profile.multiclass_image_classification.common.nn.conv',
 'offline_model_builder.content_profile.multiclass_image_classification.common.preprocessing',
 'offline_model_builder.content_profile.multiclass_image_classification.common.utils',
 'offline_model_builder.content_profile.multiclass_image_classification.config',
 'offline_model_builder.content_profile.multiclass_image_classification.data',
 'offline_model_builder.content_profile.multiclass_image_classification.data.utils',
 'offline_model_builder.repository',
 'offline_model_builder.services',
 'offline_model_builder.user_profile',
 'offline_model_builder.user_profile.clustering',
 'offline_model_builder.user_profile.clustering.evaluation',
 'offline_model_builder.user_profile.clustering.intermediate_results',
 'offline_model_builder.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.50,<2.0.0',
 'graphdb-module>=0.12.14,<0.13.0',
 'ingestor-module>=1.17.1,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'redis>=4.1.2,<5.0.0',
 'scikit-learn-extra>=0.2.0,<0.3.0',
 'scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'offline-model-builder',
    'version': '0.2.49',
    'description': 'Wrapper for offline model builder module',
    'long_description': '# rce_offline_model_builder_module\n\n',
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
