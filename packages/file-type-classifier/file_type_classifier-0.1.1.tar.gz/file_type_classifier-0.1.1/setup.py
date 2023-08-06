# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_type_classifier']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'file-type-classifier',
    'version': '0.1.1',
    'description': '',
    'long_description': '# FILE CLASSIFIER\na file  type classifier.\n\n## description \nthis library can be used to classify file types... It is made reading the file bytes and checking its bytes, not just reading the file extention.\n\n## installation \nit\'s compatible with python3.10+. To install run the command `pip install file_type_classifier`\n\n## example\n```py\nimport file_type_classifier\n\nfile_type = file_type_classifier.file_type_classifier("file_without_extention")\nprint(file_type)   # output:  png\n```\n## Author:\n<img width=\'100\' height=\'100\' style="border-radius:50%; padding:15px" src="https://avatars.githubusercontent.com/u/78698099?v=4" /></br>\n<a href="https://github.com/lipe14-ops" style=\'padding: 15px\' title="Rocketseat">Filipe Soares :computer:</a>\n<p style=\'padding: 15px\'>made with :heart: by <strong>Filipe</strong> :wave: reach me!!!</p>\n\n[![](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](fn697169@gmail.com)\n[![](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/filipe_kkkj/)\n\n',
    'author': 'lipe14-ops',
    'author_email': 'filipe.ns1001@gmai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
