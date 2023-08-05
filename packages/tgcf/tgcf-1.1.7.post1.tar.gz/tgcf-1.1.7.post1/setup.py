# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgcf', 'tgcf.bot', 'tgcf.plugins', 'tgcf.web_ui', 'tgcf.web_ui.pages']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'PyYAML>=6.0,<7.0',
 'Telethon==1.26.0',
 'aiohttp>=3.8.3,<4.0.0',
 'cryptg>=0.4.0,<0.5.0',
 'hachoir>=3.1.3,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pymongo>=4.3.3,<5.0.0',
 'pytesseract>=0.3.7,<0.4.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'streamlit>=1.15.2,<2.0.0',
 'tg-login>=0.0.4,<0.0.5',
 'typer>=0.7.0,<0.8.0',
 'verlat>=0.1.0,<0.2.0',
 'watermark.py>=0.0.3,<0.0.4']

entry_points = \
{'console_scripts': ['tgcf = tgcf.cli:app', 'tgcf-web = tgcf.web_ui.run:main']}

setup_kwargs = {
    'name': 'tgcf',
    'version': '1.1.7.post1',
    'description': 'The ultimate tool to automate custom telegram message forwarding.',
    'long_description': '<!-- markdownlint-disable -->\n\n<p align="center">\n<a href = "https://github.com/aahnik/tgcf" > <img src = "https://user-images.githubusercontent.com/66209958/115183360-3fa4d500-a0f9-11eb-9c0f-c5ed03a9ae17.png" alt = "tgcf logo"  width=120> </a>\n</p>\n\n<h1 align="center"> tgcf </h1>\n\n<p align="center">\nThe ultimate tool to automate custom telegram message forwarding.\n</p>\n\n<p align="center">\n<a href="https://github.com/aahnik/tgcf/blob/main/LICENSE"><img src="https://img.shields.io/github/license/aahnik/tgcf" alt="GitHub license"></a>\n<a href="https://github.com/aahnik/tgcf/stargazers"><img src="https://img.shields.io/github/stars/aahnik/tgcf?style=social" alt="GitHub stars"></a>\n<a href="https://github.com/aahnik/tgcf/issues"><img src="https://img.shields.io/github/issues/aahnik/tgcf" alt="GitHub issues"></a>\n<img src="https://img.shields.io/pypi/v/tgcf" alt="PyPI">\n<a href="https://twitter.com/intent/tweet?text=Wow:&amp;url=https%3A%2F%2Fgithub.com%2Faahnik%2Ftgcf"><img src="https://img.shields.io/twitter/url?style=social&amp;url=https%3A%2F%2Fgithub.com%2Faahnik%2Ftgcf" alt="Twitter"></a>\n</p>\n<p align="center">\n<a href="https://github.com/aahnik/tgcf/actions/workflows/quality.yml"><img src="https://github.com/aahnik/tgcf/actions/workflows/quality.yml/badge.svg" alt="Code Quality"></a>\n</p>\n\nLive-syncer, Auto-poster, backup-bot, cloner, chat-forwarder, duplicator, ...\n\nCall it whatever you like! tgcf can fulfill your custom needs.\n\n## Videos\n\n<!-- markdownlint-enable -->\n\nThe following videos (english) explain everything in great detail.\n\n- [Feature Overview](https://youtu.be/FclVGY-K70M)\n- [Running on Windows/Mac/Linux](https://youtu.be/5GzHb6J7mc0)\n- Running on Android\n- [Deploy to Digital Ocean Droplet](https://youtu.be/0p0JkJpfTA0)\n\n## Supported environments\n\n- Linux\n- Mac\n- Windows (Running Ubuntu on top of WSL-2)\n- Android (Using Termux app)\n- Any Linux VPS\n\n## Install and Run\n\nIf you want to use tgcf for free, then run on your own desktop or mobile computer.\n\nMake sure you are on a supported environment and have python:3.10 or above, installed.\n\n- Create a directory and move into it.\n\n  ```shell\n  mkdir my-tgcf\n  cd my-tgcf\n  ```\n\n- Create a python virtual environment and activate it.\n\n  ```shell\n  python3 -m venv .venv\n  source .venv/bin/activate\n  ```\n\n- Install tgcf using `pip`\n\n  ```shell\n  pip install tgcf\n  tgcf --version\n  ```\n\n- Set the password for accessing web interface.\n  The password is to be set in the `.env` file.\n\n  ```shell\n  echo "PASSWORD=hocus pocus qwerty utopia" >> .env\n  ```\n\n  Set your own password, instead of whats given above.\n\n  _Security advice_:\n\n  - Please make sure the password has more than 16 characters.\n  - You can save your password in any password manager (may be of browser)\n    to autofill password everytime.\n\n- Start the web-server.\n\n  ```shell\n  tgcf-web\n  ```\n\nTo run tgcf without the web-ui read about\n[tgcf cli](https://github.com/aahnik/tgcf/wiki/CLI-Usage).\n\nIf you are planning to use watermarking and ocr features within tgcf,\nyou need to install `ffmpeg` and `tesseract-ocr` libraries in you system.\n[Read more](https://github.com/aahnik/tgcf/wiki/Additional-Requirements).\n\n## Deploy to Cloud\n\nClick on [this link](https://m.do.co/c/98b725055148) and get **free 200$**\non Digital Ocean.\n\n[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=98b725055148&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)\n\n> **NOTE** You will get nothing if you directly sign up from Digital Ocean Home Page.\n> **Use the link** above, or **click on the big fat button** above to get free 200$.\n\nDeploying to a cloud server is an easier alternative if you cannot install\non your own machine.\nCloud servers are very reliable and great for running `tgcf` in live mode\nfor a long time.\n\nHere are some guides for deployment to different cloud providers.\n\n- [Heroku](https://github.com/aahnik/tgcf/wiki/Deploy-to-Heroku)\n- [Digital Ocean](https://github.com/aahnik/tgcf/wiki/Deploy-to-Digital-Ocean)\n- [Gitpod](https://github.com/aahnik/tgcf/wiki/Run-for-free-on-Gitpod")\n- [Python Anywhere](https://github.com/aahnik/tgcf/wiki/Run-on-PythonAnywhere)\n- [Google Cloud Run](https://github.com/aahnik/tgcf/wiki/Run-on-Google-Cloud)\n\n## Getting Help\n\n- First of all [read the wiki](https://github.com/aahnik/tgcf/wiki)\n  and [watch the videos](https://www.youtube.com/channel/UCcEbN0d8iLTB6ZWBE_IDugg)\n  to get started.\n\n- Type your question in GitHub\'s Search bar on the top left of this page,\n  and click "In this repository".\n  Go through the issues, discussions and wiki pages that appear in the result.\n  Try re-wording your query a few times before you give up.\n\n- If your question does not already exist,\n  feel free to ask your questions in the\n  [Discussion forum](https://github.com/aahnik/tgcf/discussions/new).\n  Please avoid duplicates.\n\n- For reporting bugs or requesting a new feature please use the [issue tracker](https://github.com/aahnik/tgcf/issues/new)\n  of the repo.\n\n## Contributing\n\nPRs are most welcome! Read the [contributing guidelines](/.github/CONTRIBUTING.md)\nto get started.\n\nIf you are not a developer, you may also contribute financially to\nincentivise the development of any custom feature you need.\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aahnik/tgcf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
