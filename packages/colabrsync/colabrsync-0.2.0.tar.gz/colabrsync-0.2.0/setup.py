# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colabrsync']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'colabrsync',
    'version': '0.2.0',
    'description': 'Run rsync periodically in the background on Google Colab.',
    'long_description': "# colabrsync\n\nRun rsync periodically in the background on Google Colab.\n\n## Usage\n\n```python\n!pip install colabrsync\n\nfrom google.colab import drive\ndrive.mount('/content/drive')\n\n!mkdir -p /content/outputs\n!mkdir -p /content/drive/MyDrive/outputs\n\nfrom colabrsync import RsyncMirror\n\nrsm = RsyncMirror('/content/outputs/', '/content/drive/MyDrive/outputs/')\n\n!diff -ur /content/outputs /content/drive/MyDrive/outputs\n\n!touch /content/outputs/newfile.txt\n\n!diff -ur /content/outputs /content/drive/MyDrive/outputs\n\n!sleep 60\n\n!diff -ur /content/outputs /content/drive/MyDrive/outputs\n\ndel rsm\n\n!ls -l /content/outputs /content/drive/MyDrive/outputs\n```\n\n## License\n\nMIT License, See LICENSE file.\n\n## Author\n\nSusumu OTA\n",
    'author': 'Susumu OTA',
    'author_email': '1632335+susumuota@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/susumuota/colabrsync',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
