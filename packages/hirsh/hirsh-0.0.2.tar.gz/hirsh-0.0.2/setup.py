# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hirsh', 'hirsh.entities', 'hirsh.repositories', 'hirsh.services']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy[asyncio,mypy]>=1.4.44,<2.0.0',
 'aiogram>=2.23.1,<3.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'dependency-injector>=4.40.0,<5.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'typer>=0.7.0,<0.8.0',
 'uvloop>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'hirsh',
    'version': '0.0.2',
    'description': 'Resilient monitoring system that detects utility outages in unreliable environments (e.g. IoT, RaspberryPi, etc)',
    'long_description': "# Hirsh\n\n📟 Resilient monitoring system that detects utility outages in unreliable environments (e.g. IoT, RaspberryPi, etc).\n\nHirsh is designed and optimized for:\n\n- 💪 residency, robustness and self-healing \n- 📟 running in resource-constrained IoT-like unstable environments\n\n## Maturity\n\nThe project is in early MVP state. \n\nIt's being actively tested using my RaspberryPi Zero 2W under the current unstable Ukrainian infrastructure conditions.\n\n## Setups\n\nHirsh can be executed in any IoT device or board computer that supports Linux-like OS and Python 3.9+.\n\n- [Only Supported] Basic: The basic setup includes just the device.\n    The device is plugged into the main electricity circuit/outlet along with a router that provides network connection for the device.\n- UPS: TBU\n\n## Monitors\n\nIn theory, you can track any utilities your home has (e.g. electricity, network, gas, water, etc.). \nHowever, in practice it's the easiest to track:\n\n- network connection [Only Supported]\n- electricity supply\n\n## How does it work?\n\nTBU\n\n## Notifications\n\n### Telegram\n\nThe primary way to notify you about outages is via [Telegram bot](https://core.telegram.org/bots).\nYou need to create [a new bot](https://t.me/BotFather) and add it to a group or a channel.\n\n## References\n\n### Similar Projects\n\n- https://github.com/fabytm/Outage-Detector\n- https://github.com/nestukh/rpi-powerfail\n- https://www.kc4rcr.com/power-outage-notification/\n- https://homediyelectronics.com/projects/raspberrypi/poweroffdelay/powerfail\n- https://projects-raspberry.com/power-outage-sensor/\n- https://raspberrypi.stackexchange.com/questions/13538/raspberry-pi-to-email-when-power-outage-occurs\n\n### Python + RPi\n\n- https://medium.com/geekculture/gpio-programming-on-the-raspberry-pi-python-libraries-e12af7e0a812\n\n### AsyncIO and RPi\n\n- https://github.com/PierreRust/apigpio\n- https://beenje.github.io/blog/posts/experimenting-with-asyncio-on-a-raspberry-pi/\n- https://www.digikey.bg/en/maker/projects/getting-started-with-asyncio-in-micropython-raspberry-pi-pico/110b4243a2f544b6af60411a85f0437c\n- https://docs.micropython.org/en/latest/library/uasyncio.html\n\n### Deployment\n\n- https://github.com/beenje/legomac",
    'author': 'Roman Glushko',
    'author_email': 'roman.glushko.m@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
