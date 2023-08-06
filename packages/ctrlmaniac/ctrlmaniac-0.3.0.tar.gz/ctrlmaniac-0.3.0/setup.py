# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctrlmaniac']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ctrlmaniac',
    'version': '0.3.0',
    'description': "Davide DC's GitHub Readme profile",
    'long_description': '# Davide Di Criscito\n\n```python\nclass CtrlManiac:\n    """CtrlManiac because i overuse the ctrl key."""\n\n    def __init__(self):\n        """My specifications."""\n        self.name = "Davide"\n        self.surname = "Di Criscito"\n        self.nickname = "Dave"\n        self.pronouns = (\n            "He",\n            "Him",\n        )\n\n        self.languages_spoken = ["it_IT", "en_US", "en_GB"]\n\n        self.description = (\n            "I\'m currently an Artisan, soon-to-be a full-stack web developer!"\n        )\n\n        self.websites = [\n            "https://ctrlmaniac.me",\n            "https://www.linkedin.com/in/dcdavide/",\n        ]\n\n        self.hobbies = [\n            "coding",\n            "hiking",\n            "photography",\n            "watching movies & TV series",\n            "listening to music",\n            "reading books and manga",\n            "going out with my friends and have fun",\n        ]\n\n        self.coding_languages = [\n            "Python",  # I simply love it\n            "JavaScript",\n            "Typescript",\n            "Java",\n            "Golang",\n        ]\n\n        self.favourite_tools = [\n            "poetry",  # makes it simpler to manage a python project\n            "black",  # chooses a coding style for me and makes my code pretty\n            "isort",  # sorts python imports so that everything is really clear\n            "flake8",  # tells me whether I\'ve made a mistake\n            "pydocstyle",  # helps me write better documentation\n            "yarn",  # I love it for the workspace feature\n            "lerna",  # I use it to manage my monorepos\n            "prettier",  # chooses a coding style for me and makes my code pretty\n        ]\n\n        self.IDEs = [\n            "VScode",  # because it\'s awesome!\n        ]\n\n    def greet(self) -> None:\n        """Say hi."""\n        print(\n            f"Hi! I\'m {self.name} {self.surname}, but you can call me {self.nickname}."\n        )\n        print(self.description)\n        print(f"You can know more about me by visiting my website: {self.website}")\n```\n\n## Fun Fact\n\nYou can install this package via pip by running `pip install ctrlmaniac` and then excecute the program by typing into your terminal `python -m ctrlmaniac` and see the output!\n\nOr import the package:\n\n```\n>>> from ctrlmaniac import ctrlmaniac\n>>> me = ctrlmaniac.CtrlManiac()\n\n>>> me.greet()\nHi! I\'m Davide Di Criscito, but you can call me Dave.\nI\'m currently an Artisan, soon-to-be a full-stack web developer!\nYou can know more about me by visiting my website: https://ctrlmaniac.me\n```\n\n## Stats\n\n[![Anurag\'s GitHub stats](https://github-readme-stats.vercel.app/api?username=ctrlmaniac)](https://github.com/anuraghazra/github-readme-stats)\n[![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=ctrlmaniac)](https://github.com/anuraghazra/github-readme-stats)\n',
    'author': 'Davide Di Criscito',
    'author_email': 'davide.dicriscito@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
