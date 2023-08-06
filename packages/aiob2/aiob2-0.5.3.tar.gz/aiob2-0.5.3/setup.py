# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiob2', 'aiob2.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'pytest-asyncio>=0.19.0,<0.20.0',
 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'aiob2',
    'version': '0.5.3',
    'description': "A simple and easy to use async wrapper for Backblaze's B2 bucket API.",
    'long_description': '# aiob2\n\n---\n\n<p align="center">\n    <a href="https://www.python.org/downloads/">\n        <img src="https://img.shields.io/pypi/pyversions/aiob2?style=for-the-badge" alt="Python version">\n    </a>\n    <a href="https://github.com/Void-ux/aiob2/actions">\n        <img src="https://img.shields.io/github/actions/workflow/status/Void-ux/aiob2/build.yaml?branch=master&style=for-the-badge" alt="Build status">\n    </a>\n    <a href="https://pypi.org/project/aiob2/">\n        <img src="https://img.shields.io/pypi/v/aiob2?color=8BC34A&style=for-the-badge" alt="PyPi">\n    </a>\n    <a href="https://opensource.org/licenses/MIT">\n        <img src="https://img.shields.io/pypi/l/aiob2?color=C0C0C0&style=for-the-badge" alt="License">\n    </a>\n</p>\n\naiob2 is an asynchronous API wrapper for the [Backblaze B2 Bucket API](https://www.backblaze.com/b2/docs/calling.html).\n\nIt will allow you to interact with your B2 bucket, it\'s files and anything else that the B2 API allows in a modern, object-oriented fashion.\n\n__**NOTE:**__ This API wrapper is by no means *complete* and has many endpoints to cover, though the main ones have been covered (they will be listed below)\n\n## Installation\n\n---\n\naiob2 is compatible with Python 3.8+ (this is an estimate). To install aiob2, run the following command in your (virtual) environment.\n\n```\npip install aiob2\n```\n\nAlternatively, for the latest though least stable version, you can download it from the GitHub repo:\n\n```\npip install git+https://github.com/Void-ux/aiob2.git\n```\n\n## Usage\n\n### Uploading\n\n```python\nimport aiohttp\nimport asyncio\n\nfrom aiob2 import Client\n\n# Our image to upload to our bucket\nwith open(r\'C:\\Users\\MS1\\Pictures\\Camera Roll\\IMG_5316.jpeg\', \'rb\') as file:\n    data = file.read()\n\nasync def main():\n    async with Client(\'key_id\', \'key\') as client:\n        file = await client.upload_file(\n            content_bytes=data,\n            content_type=\'image/jpeg\',\n            file_name=\'test.jpg\',\n            bucket_id=\'bucket_id\',\n        )\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\nAnd that\'s it! `upload_file()` returns a `File` object that neatly wraps everything Backblaze\'s API has provided us with.\nThe `File` object\'s documentation can be found [here](https://aiob2.readthedocs.io/en/latest/pages/api.html#aiob2.File)\n\n## License\n\n---\n\nThis project is released under the [MIT License](https://opensource.org/licenses/MIT).\n',
    'author': 'Dan',
    'author_email': 'the.void.altacc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Void-ux/aiob2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
