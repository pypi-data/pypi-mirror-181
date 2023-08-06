# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tkl']
install_requires = \
['leds>=3.5.1,<4.0.0', 'requests>=2.28.1,<3.0.0', 'xled>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'tkl',
    'version': '0.9.0',
    'description': 'A leds/bibliopixel driver for Twinkly lights',
    'long_description': "tkl: Twinkly driver for `leds`/`Bibliopixel`\n-----------------------------------------------------\n\nInstall using `pip install tkl`.\n\nTest from the command line with:\n\n.. code-block:: bash\n\n    leds '{driver: tkl, animation: BiblioPixelAnimations.strip.ColorChase}'\n\n    # or for legacy systems using BiblioPixel\n    bp '{driver: tkl, animation: BiblioPixelAnimations.strip.ColorChase}'\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
