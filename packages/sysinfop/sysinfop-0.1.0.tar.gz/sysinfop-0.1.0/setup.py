# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sysinfop']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.9.4,<6.0.0', 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['sysinfop = sysinfop:console.run']}

setup_kwargs = {
    'name': 'sysinfop',
    'version': '0.1.0',
    'description': 'Lightweight system info grabber',
    'long_description': 'sysinfop\n========\n\nLightweight system info utility\n\n   Sysinfop is my own attempt at a *Neofetch* / *Screenfetch* style cli\n   app. Sysinfop Is built using Python3 and requires both a working\n   Python3 install as well as the Poetry build tool available on your\n   system if you are building the project from source. Pre-built\n   ``wheel``, ``sdist``, ``.exe`` (Windows), and ``.app`` (MacOS) assets\n   will be available soon...\n\nWhat does it look like?\n-----------------------\n\nOn a 2022 Macbook Air for example, it will output the following.\n\n.. code:: shell\n\n     hostname.local\n     * IP: 127.0.0.1\n     * OS: Darwin\n     * CPU: arm\n     * RAM: 8 GB\n\nHow to use it\n-------------\n\nSimply call ``sysinfop`` from your shell configuration.\n\nbash\n~~~~\n\n.. code:: shell\n\n   $ echo "sysinfop" >> ~/.bashrc\n\nzsh\n~~~\n\n.. code:: shell\n\n   $ echo "sysinfop" >> ~/.zshrc\n\nHow to install it\n-----------------\n\nInstall from pip\n~~~~~~~~~~~~~~~~\n\n.. code:: shell\n\n   pip install sysinfop\n\nContributing\n------------\n\nThe project is a simple Python 3 app that is built using the Poetry\ntool, this is all you need to contribute. PR\'s, issues, etc. all\ndirected to this github repo.\n\nLICENSE\n-------\n\nMIT License\n\nCopyright (c) 2022 Josh Burns josh@joshhburns.xyz\n\nPermission is hereby granted, free of charge, to any person obtaining a\ncopy of this software and associated documentation files (the\n"Software"), to deal in the Software without restriction, including\nwithout limitation the rights to use, copy, modify, merge, publish,\ndistribute, sublicense, and/or sell copies of the Software, and to\npermit persons to whom the Software is furnished to do so, subject to\nthe following conditions:\n\nThe above copyright notice and this permission notice shall be included\nin all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS\nOR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\nIN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY\nCLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,\nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE\nSOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'Josh Burns',
    'author_email': 'joshyburnss@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
