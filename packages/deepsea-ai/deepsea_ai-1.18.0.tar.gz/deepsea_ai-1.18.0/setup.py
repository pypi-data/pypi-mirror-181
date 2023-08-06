# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepsea_ai',
 'deepsea_ai.commands',
 'deepsea_ai.config',
 'deepsea_ai.database',
 'deepsea_ai.pipeline',
 'deepsea_ai.tests']

package_data = \
{'': ['*']}

install_requires = \
['awscli>=1.25.71,<2.0.0',
 'boto3>=1.24.70,<2.0.0',
 'click>=8.0.0,<9.0.0',
 'requests>=2.26.0,<3.0.0',
 'sagemaker>=2.102.0,<3.0.0',
 'tqdm>=4.41.0,<5.0.0']

entry_points = \
{'console_scripts': ['deepsea-ai = deepsea_ai.__main__:cli']}

setup_kwargs = {
    'name': 'deepsea-ai',
    'version': '1.18.0',
    'description': 'DeepSeaAI is a Python package to simplify processing deep sea video in AWS from a command line.',
    'long_description': '[![MBARI](https://www.mbari.org/wp-content/uploads/2014/11/logo-mbari-3b.png)](http://www.mbari.org)\n[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)\n![license-GPL](https://img.shields.io/badge/license-GPL-blue)\n[![Python](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/downloads/)\n\n**DeepSeaAI** is a Python package to simplify processing deep sea video in [AWS](https://aws.amazon.com) from a command line. \n \nIt includes reasonable defaults that have been optimized for deep sea video. The goal is to simplify running these algorithms in AWS.\n\nDeepSea-AI currently supports:\n\n - *Training [YOLOv5](http://github.com/ultralytics/yolov5) object detection* models\n - *Processing video with [YOLOv5](http://github.com/ultralytics/yolov5) detection and tracking pipelines* using either:\n     * [DeepSort](https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch) tracking\n     * [StrongSort](https://github.com/mikel-brostrom/Yolov5_StrongSORT_OSNet) tracking\n\n## Install\n\nSetup [an AWS account](https://aws.amazon.com).\n\nAfter you have setup your AWS account, configure it using the awscli tool, and confirm your AWS Account by listing your s3 buckets\n\n```\npip install awscli\naws configure\naws --version\naws s3 ls \n```\n\nInstall and update using [pip](https://pip.pypa.io/en/stable/getting-started/) in a Python>=3.8.0 environment:\n\n```shell\npip install -U deepsea-ai\n```\n\nSetup your AWS account for use with this module with\n\n```shell\ndeepsea-ai setup\n```\n\n\n\n## Tutorials\n\n* [FathomNet](docs/notebooks/fathomnet_train.ipynb) ✨ Recommended first step to learn more about how to train a YOLOv5 object detection model using freely available FathomNet data\n\nThe best way to use the tutorials is with [Anaconda](https://www.anaconda.com/products/distribution).\n\n### Create the Anaconda environment\n\nThis will create an environment called *deepsea-ai-notebooks* and make that available in your local jupyter notebook as the kernel named *deepsea-ai-notebooks*\n```\nconda env create \nconda activate deepsea-ai-notebooks\npip install ipykernel\npython -m ipykernel install --user --name=deepsea-ai-notebooks\n```\n\n### Launch jupyter\n\n```\ncd docs/notebooks\njupyter notebook\n```\n---\n\n## Commands\n\n* `deepsea-ai setup --help` - Setup the AWS environment. Must run this once before any other commands.\n* [`deepsea-ai train --help` - Train a YOLOv5 model and save the model to a bucket](commands/train.md)\n* [`deepsea-ai process --help` - Process one or more videos and save the results to  a bucket](commands/process.md)\n* [`deepsea-ai ecsprocess --help` - Process one or more videos using the Elastic Container Service and save the results to a bucket](commands/process.md)\n* [`deepsea-ai split --help` - Split your training data. This is required before the train command.](data.md) \n* `deepsea-ai -h` - Print help message and exit.\n \nSource code is available at [github.com/mbari-org/deepsea-ai](https://github.com/mbari-org/deepsea-ai/).\n  \nFor more details, see the [official documentation](http://docs.mbari.org/deepsea-ai/install).',
    'author': 'Danelle Cline',
    'author_email': 'dcline@mbari.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mbari-org/deepsea-ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
