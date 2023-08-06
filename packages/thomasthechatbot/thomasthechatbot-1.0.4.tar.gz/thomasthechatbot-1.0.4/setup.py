# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ttc', 'ttc.chatbot', 'ttc.cli']

package_data = \
{'': ['*']}

install_requires = \
['contractions>=0.1.72,<0.2.0',
 'fastpunct>=2.0.2,<3.0.0',
 'inquirerpy>=0.3.4,<0.4.0',
 'nltk>=3.7,<4.0',
 'pyspellchecker>=0.7.0,<0.8.0',
 'torch==1.12.1',
 'typer>=0.6.1,<0.7.0',
 'yaspin>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['ttc = ttc.cli.main:app']}

setup_kwargs = {
    'name': 'thomasthechatbot',
    'version': '1.0.4',
    'description': 'A Python chatbot that learns as you speak to it.',
    'long_description': '<div align="center">\n    <img src="https://i.imgur.com/hA9YF2s.png" alt="Thomas" width="220" height="220">\n    <h1>Thomas the Chatbot</h1>\n</div>\n\n![Demo](https://i.imgur.com/Jet4UGh.gif)\n\n# Installation\n\n**Python 3.9+ is required**\n\nThis package can be installed from [PyPi](https://pypi.org/project/thomasthechatbot/) with:\n\n```\npip install thomasthechatbot\n```\n\n## CLI\n\nType `ttc` to begin talking to Thomas.\n\n# How does Thomas work?\n\nI wrote a [medium article](https://medium.com/@principle105/creating-a-python-chatbot-that-learns-as-you-speak-to-it-60b305d8f68f) to explain how Thomas works.\n\n# Usage\n\n## Basic Usage\n\n```py\nfrom ttc import Chatbot, Context, download_nltk_data\n\n# Only needs to be run once (can be removed after first run)\ndownload_nltk_data()\n\n# Creating the context\nctx = Context()\n\n# Initializing the chatbot\nchatbot = Chatbot()\n\ntalk = True\n\nwhile talk:\n    msg = input("You: ")\n\n    if msg == "s":\n        talk = False\n    else:\n        # Getting the response\n        resp = chatbot.respond(ctx, msg)\n\n        # Saving the response to the context\n        ctx.save_resp(resp)\n\n        print(f"Thomas: {resp}")\n\n# Saving the chatbot data\nchatbot.save_data()\n```\n\n## Configurations\n\n```py\nchatbot = Chatbot(\n    path="brain",\n    learn=False,\n    min_score=0.5,\n    score_threshold=0.5,\n    mesh_association=0.5,\n)\n```\n\n# Contributing\n\nOpen to contributions, please create an issue if you want to do so.\n\n# Formatting\n\n[Black](https://github.com/psf/black), [isort](https://github.com/PyCQA/isort) and [Prettier](https://prettier.io/) are used for formatting\n',
    'author': 'principle105',
    'author_email': 'principle105@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/principle105/thomasthechatbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
