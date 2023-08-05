# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vivintpy', 'vivintpy.devices']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'certifi>=2022.9.24,<2023.0.0', 'pubnub>=7.0,<8.0']

setup_kwargs = {
    'name': 'vivintpy',
    'version': '2022.12.1',
    'description': 'Python library for interacting with a Vivint security and smart home system.',
    'long_description': "[![pypi](https://img.shields.io/pypi/v/vivintpy?style=for-the-badge)](https://pypi.org/project/vivintpy)\n[![downloads](https://img.shields.io/pypi/dm/vivintpy?style=for-the-badge)](https://pypi.org/project/vivintpy)\n[![Buy Me A Coffee/Beer](https://img.shields.io/badge/Buy_Me_A_☕/🍺-F16061?style=for-the-badge&logo=ko-fi&logoColor=white&labelColor=grey)](https://ko-fi.com/natekspencer)\n\n# vivintpy\n\nPython library for interacting with a Vivint security and smart home system.\n\nThis was built to support the `Vivint` integration in [Home-Assistant](https://www.home-assistant.io/) but _should_ work outside of it too. Currently, it can be utilized via [HACS](https://hacs.xyz/) by adding the [hacs-vivint](https://github.com/natekspencer/hacs-vivint) custom repository.\n\n## Credit\n\nThis was inspired by the great work done by [Mike Reibard](https://github.com/Riebart/vivint.py) to reverse engineer the Vivint Sky API and [Ovidiu Stateina](https://github.com/ovirs/pyvivint) for the repository from which this is forked and expanded on.\n\n## Features\n\nIt currently has support for the following device types:\n\n- alarm panels\n- cameras\n- door locks\n- garage doors\n- switches\n  - binary\n  - multilevel\n- thermostats\n- wireless sensors\n  - carbon monoxide\n  - door/window\n  - flood\n  - glass break\n  - motion\n  - smoke/fire\n  - etc\n\nIn addition, it integrates with PubNub to receive real-time updates for devices. This subscription stops receiving notifications around 15-20 minutes unless a call is made to the Vivint Sky API periodically. This **might** be related to the cookie expiration since it expires 20 minutes after the last API call was received. If another client connects, however, the notifications start to stream again for all currently connected clients.\n\n## Usage\n\nSee demo.py for a demonstration on how to use this library.\n\n## TODO:\n\n- write a better readme\n- write some documentation\n- add advanced support for:\n  - thermostats\n- add tests\n\n---\n\n## Support Me\n\nI'm not employed by Vivint, and provide this python package as-is.\n\nIf you don't already own a Vivint system, please consider using [my referal code (kaf164)](https://www.vivint.com/get?refCode=kaf164&exid=165211vivint.com/get?refCode=kaf164&exid=165211) to get $50 off your bill (as well as a tip to me in appreciation)!\n\nIf you already own a Vivint system and still want to donate, consider buying me a coffee ☕ (or beer 🍺) instead by using the link below:\n\n<a href='https://ko-fi.com/natekspencer' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' />\n",
    'author': 'Nathan Spencer',
    'author_email': 'natekspencer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/natekspencer/vivintpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
